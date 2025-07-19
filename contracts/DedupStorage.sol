// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DedupStorage {
    struct FileData {
        string sha256;     // SHA-256 hash
        string phash;      // Perceptual hash
        string ipfsCID;    // IPFS content identifier
        address uploader;  // Address who uploaded the file
        uint256 timestamp; // Upload time
    }

    // Mapping of SHA-256 hash => FileData
    mapping(string => FileData) private storedFiles;
    mapping(string => bool) public sha256Exists;
    mapping(string => bool) public phashExists;

    event FileStored(string sha256Hash, string phash, string ipfsCID, address indexed uploader, uint256 timestamp);

    // Store a new file if it doesn’t exist
    function storeFile(string memory sha256Hash, string memory phash, string memory ipfsCID) public {
        require(!sha256Exists[sha256Hash], "Duplicate file: SHA-256 hash already exists");
        require(!phashExists[phash], "Duplicate file: visually similar image exists");
        storedFiles[sha256Hash] = FileData({
            sha256: sha256Hash,
            phash: phash,
            ipfsCID: ipfsCID,
            uploader: msg.sender,
            timestamp: block.timestamp
        });
        sha256Exists[sha256Hash] = true;
        phashExists[phash] = true;
        emit FileStored(sha256Hash, phash, ipfsCID, msg.sender, block.timestamp);
    }

    // Check if file exists by SHA-256 or phash
    function fileExists(string memory sha256Hash, string memory phash) public view returns (bool, string memory) {
        if (sha256Exists[sha256Hash]) {
            return (true, "Exact match found (SHA-256)");
        }
        if (phashExists[phash]) {
            return (true, "Visually similar match found (phash)");
        }
        return (false, "No match found");
    }

    // Get file data by SHA-256 hash
    function getFile(string memory sha256Hash) public view returns (string memory, string memory, string memory, address, uint256) {
        require(sha256Exists[sha256Hash], "File not found");
        FileData memory file = storedFiles[sha256Hash];
        return (file.sha256, file.phash, file.ipfsCID, file.uploader, file.timestamp);
    }
}