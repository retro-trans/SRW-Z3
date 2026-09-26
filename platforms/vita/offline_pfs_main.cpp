// Local adapter for Vita3K/psvpfsparser; no networking or secret CLI values.
// Compile core sources only; exclude upstream CLI/zRIF/cache backends.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstring>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <memory>
#include <streambuf>
#include "OpenSSLCryptoOperations.h"
#include "F00DNativeKeyEncryptor.h"
#include "PfsFilesystem.h"
#include "LocalKeyGenerator.h"

struct NullBuffer : std::streambuf {
    int overflow(int ch) override { return traits_type::not_eof(ch); }
};

int main(int argc, char **argv) {
    // source-directory destination-directory license-file [--write]
    if (argc < 4 || argc > 5) {
        std::cerr << "Usage: offline_pfs source destination license-file [--write]\n";
        return 2;
    }
    namespace fs = std::filesystem;
    fs::path src = fs::absolute(argv[1]), dst = fs::absolute(argv[2]);
    std::array<unsigned char, 512> rif{};
    std::ifstream in(argv[3], std::ios::binary);
    if (!in.read(reinterpret_cast<char*>(rif.data()), rif.size()) || in.peek() != EOF ||
        !fs::exists(src / "sce_pfs/files.db") || !fs::exists(src / "sce_pfs/unicv.db") || fs::exists(dst)) {
        std::cerr << "Invalid source/license or destination already exists.\n";
        return 2;
    }
    if (std::memcmp(rif.data() + 0x17, "PCSG00264", 9) != 0 ||
        std::all_of(rif.begin() + 0x50, rif.begin() + 0x60, [](unsigned char v){ return v == 0; })) {
        std::cerr << "Unexpected license identity or missing key.\n";
        return 2;
    }
    if (argc == 4) {
        std::cout << "Dry-run: mount and decrypt PCSG00264 into a NEW directory; native offline crypto.\n";
        std::cout << "No key arguments, no key/cache logging, originals unchanged. Add --write.\n";
        return 0;
    }
    if (std::strcmp(argv[4], "--write") != 0) return 2;
    NullBuffer nullbuf;
    std::ostream quiet(&nullbuf);
    // Core diagnostics sometimes use cout directly; discard them too.
    // Never buffer unknown upstream output, which could contain derived keys.
    auto *oldcout = std::cout.rdbuf(&nullbuf);
    auto *oldcerr = std::cerr.rdbuf(&nullbuf);
    std::ostream status(oldcout);
    int result = 1, phase = 0;
    try {
        auto crypto = std::make_shared<OpenSSLCryptoOperations>();
        auto native = std::make_shared<F00DNativeKeyEncryptor>(crypto);
        PfsFilesystem pfs(crypto, native, quiet, rif.data() + 0x50, src);
        phase = 1;
        if (pfs.mount() == 0) {
            status << "PFS metadata/signature checks passed. Decrypting files...\n" << std::flush;
            phase = 2;
            fs::create_directory(dst);
            unsigned int last = 0;
            auto progress = [&](std::uint64_t done, std::uint64_t total, const std::string&) {
                unsigned int percent = total ? static_cast<unsigned int>(done * 100 / total) : 0;
                if (percent >= last + 10) {
                    last = percent;
                    status << "Decryption: " << percent << "%\n" << std::flush;
                }
            };
            if (pfs.decrypt_files(dst, progress) == 0) {
                phase = 3;
                if (get_keystone(crypto, dst) == 0) result = 0;
            }
        }
    } catch (...) { result = 1; } // no exception content, potentially sensitive
    std::fill(rif.begin(), rif.end(), 0);
    std::cout.rdbuf(oldcout);
    std::cerr.rdbuf(oldcerr);
    std::cout << "Offline PFS result: " << (result == 0 ? "PASS" : "FAIL")
              << "; phase=" << phase << " (1=mount, 2=files, 3=keystone).\n";
    return result;
}
