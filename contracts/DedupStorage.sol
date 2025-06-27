// SPDX-License-Identifier: MIT
pragma solidity ^0.8.30;

contract DedupStorage {
    struct FileData {
        string ipfsCID;     // The IPFS content identifier
        address uploader;   // Address who uploaded the file
        uint256 timestamp;  // Upload time
    }

    // Mapping of SHA-256 hash => FileData
    mapping(string => FileData) private storedFiles;

    // To check existence
    mapping(string => bool) public fileExists;

    event FileStored(string sha256Hash, string ipfsCID, address indexed uploader, uint256 timestamp);

    // Store a new file if it doesn’t exist
    function storeFile(string memory sha256Hash, string memory ipfsCID) public {
        require(!fileExists[sha256Hash], "Duplicate file: hash already exists");

        storedFiles[sha256Hash] = FileData({
            ipfsCID: ipfsCID,
            uploader: msg.sender,
            timestamp: block.timestamp
        });

        fileExists[sha256Hash] = true;

        emit FileStored(sha256Hash, ipfsCID, msg.sender, block.timestamp);
    }

    // Get file data by SHA256 hash
    function getFile(string memory sha256Hash) public view returns (string memory ipfsCID, address uploader, uint256 timestamp) {
        require(fileExists[sha256Hash], "File not found");
        FileData memory file = storedFiles[sha256Hash];
        return (file.ipfsCID, file.uploader, file.timestamp);
    }
}
