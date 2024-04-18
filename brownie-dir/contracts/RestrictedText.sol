// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RestrictedText {
    // Variabel untuk menyimpan teks yang dibatasi
    string private restrictedText;
    
    // Mapping untuk menyimpan status akses dari setiap alamat
    mapping(address => bool) private access;
    
    // Event untuk memberi tahu ketika teks diubah
    event TextChanged(string newText, address changer);
    
    // Modifier untuk memastikan hanya pemilik kontrak yang dapat mengakses fungsi tertentu
    modifier onlyOwner() {
        require(msg.sender == owner, "Only contract owner can call this function");
        _;
    }
    
    // Alamat pemilik kontrak
    address private owner;
    
    // Konstruktor untuk menginisialisasi pemilik kontrak
    constructor() {
        owner = msg.sender;
    }
    
    // Fungsi untuk menambahkan atau menghapus akses untuk alamat tertentu
    function grantAccess(address _address, bool _allowAccess) public onlyOwner {
        access[_address] = _allowAccess;
    }
    
    // Fungsi untuk menulis teks baru (dapat diakses oleh pemilik kontrak atau alamat yang diberi akses)
    function writeText(string memory _newText) public {
        require(access[msg.sender] || msg.sender == owner, "You do not have permission to write the text");
        restrictedText = _newText;
        emit TextChanged(_newText, msg.sender);
    }
    
    // Fungsi untuk membaca teks (hanya dapat diakses oleh alamat yang diberi izin)
    function readText() public view returns (string memory) {
        require(access[msg.sender], "You do not have permission to read the text");
        return restrictedText;
    }
}
