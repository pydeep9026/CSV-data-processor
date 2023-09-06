
//YE SARE IMPORT HAIN
import React, { useState } from 'react';
import axios from 'axios'; //AXIOS BACKEND API CONNECT KRTA HAI
import './App.css';  //YE STYLING FILE KO IMPORT  KIYA HAI
import csvlogo from './csvlogo.png';  //YE LOGO HAI CSV WALA
import Toast, { Toaster } from 'react-hot-toast';  //YE WARNING KA TOAST LIBRARY HAI AGR NHI UPLOAD KROGE FILE TO E HI WARNING DIKHATA HAI


function App() {

  //YE FILE KO STORE KREGA
  const [file, setFile] = useState(null);


  // YE FUNCTION BAS INPUT SE JO FILE UPLOAD HOGA USE  FILE KE USESTATE ME DAL DEGA
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  

  const handleProcessData = async () => {


     //AGAR FILE UPLOAD NAHI KROGE TO YE  RUN HOGA
    if (!file) {
      Toast.error('Please select a file to process data');
    }

    
    const formData = new FormData();
    formData.append('file', file);



    //AXIOS AXIOS POST REQ KR RHA HAI
    try {
      const response = await axios.post('https://flask-g03o.onrender.com/process-csv', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        responseType: 'blob',
      });



      //AGR UDHR SE RESONNSE AYEGA AS XLSX TO YE DOWNLOAD WALA PART RUN HOGA
      if (response.status === 200) {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'processed_data.xlsx');
        document.body.appendChild(link);
        link.click();
      } else {
      }


    } catch (error) {
      //aur agr koi error aayega to ye run hoga
      console.log(error);
    }
  };

  return (
    <div className="container">
      <Toaster />
      <h1 className="title">CSV Data Processor</h1>
      <div className="form-container">
        <h2 className="subheader">Upload CSV File</h2>
        <label htmlFor="fileInput" className="upload-label">
          <span className="upload-text">Select CSV file</span>
          <img src={csvlogo} alt="Upload" className="upload-icon" />
          <input
            type="file"
            id="fileInput"
            className="upload-input"
            onChange={handleFileChange}
            accept=".csv"
          />
        </label>
        <button onClick={handleProcessData}>Process Data</button>
      </div>
    </div>
  );
}

export default App;
