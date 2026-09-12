const API_URL =
  import.meta.env.VITE_API_URL ||
  "http://localhost:8000";


export async function healthCheck() {

  const response =
    await fetch(
      `${API_URL}/health`
    );


  if (!response.ok) {

    throw new Error(
      "Backend is not available"
    );

  }


  return response.json();

}


export async function analyzeAudio(file) {

  const formData =
    new FormData();

  formData.append(
    "file",
    file
  );


  const response =
    await fetch(
      `${API_URL}/api/analysis/analyze`,
      {
        method: "POST",
        body: formData
      }
    );


  if (!response.ok) {

    throw new Error(
      "Audio analysis failed"
    );

  }


  return response.json();

}