import React, { useState } from 'react';
import axios from 'axios';

function FileCompression() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [compressedFileUrl, setCompressedFileUrl] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleCompress = async () => {
    const formData = new FormData();
    formData.append('file', 'test');
    //formData.append('file', selectedFile);

    try {
      const response = await axios.post('/compress', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        responseType: 'blob',
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      setCompressedFileUrl(url);

    } catch (error) {
      console.error('Error compressing file:', error);
    }
  };

  const downloadCompressedFile = () => {
    const link = document.createElement('a');
    link.href = compressedFileUrl;
    link.download = `${selectedFile.name}.gz`;
    link.click();
  };

  return (
    <div>
      <h1>File Compression</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleCompress}>Compress</button>

      {compressedFileUrl && (
        <>
          <p>Compressed file ready!</p>
          <button onClick={downloadCompressedFile}>Download</button>
        </>
      )}
    </div>
  );
}

export default FileCompression;