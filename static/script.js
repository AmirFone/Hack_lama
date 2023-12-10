let progressInterval, recordingTime, maxRecordingTime = 25000;
document.querySelector('.browse-btn').addEventListener('click', function() {
    document.querySelector('#fileInput').click();
});


function handlePDFInput(event) {
    showWebcam();
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('pdf', file);

    fetch('/text', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => console.log(data));
}

function handleTextInput() {
    showWebcam();
    const text = document.getElementById('fileInput').value;
            fetch('/text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'text=' + encodeURIComponent(text)
            })
            .then(response => response.json())
            .then(data => console.log(data));

    
}

function showWebcam() {
    document.getElementById('webcam').style.display = 'block';
    document.querySelector('.record-btn').style.display = 'inline-block';
    document.querySelector('.stop-btn').style.display = 'inline-block';
    startWebcam();
}

function startWebcam() {
    navigator.mediaDevices.getUserMedia({ video: true, audio: true })
        .then(stream => {
            const video = document.getElementById('webcam');
            video.srcObject = stream;
            video.play();

            video.muted = true;
        })
        .catch(err => {
            console.error('Error accessing the webcam', err);
        });
}

let mediaRecorder;
let recordedBlobs;

function handleDataAvailable(event) {
    if (event.data && event.data.size > 0) {
        recordedBlobs.push(event.data);
    }
}

function startRecording() {
    document.querySelector('.record-btn').disabled = true;
    recordedBlobs = [];
    const video = document.getElementById('webcam');
    let stream = video.srcObject;
    mediaRecorder = new MediaRecorder(stream, { mimeType: 'video/webm; codecs=vp8,opus' });
    mediaRecorder.ondataavailable = handleDataAvailable;
    mediaRecorder.start();

    // Start the progress indicator
    const recordProgress = document.getElementById('recordProgress');
    const timer = document.getElementById('timer');
    recordProgress.style.width = '0%';
    recordingTime = 0;
    timer.textContent = '00:00';
    progressInterval = setInterval(() => {
        recordingTime += 1000;
        const progress = (recordingTime / maxRecordingTime) * 100;
        recordProgress.style.width = progress + '%';
        let seconds = Math.floor((recordingTime / 1000) % 60);
        let minutes = Math.floor((recordingTime / (1000 * 60)) % 60);
        timer.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        if (recordingTime >= maxRecordingTime) {
            clearInterval(progressInterval);
            stopRecording();
        }
    }, 1000);
}

function stopRecording() {
    document.querySelector('.record-btn').disabled = false;
    mediaRecorder.stop();
    clearInterval(progressInterval); // Stop the progress indicator

    // Wait for the MediaRecorder to stop before creating the blob
    mediaRecorder.onstop = () => {
        const blob = new Blob(recordedBlobs, { type: 'video/webm' });
        console.log("Blob size: " + blob.size + " bytes");

        // Send the recorded video to the Flask endpoint
        const formData = new FormData();
        formData.append('video', blob);
        fetch('/video', {
            method: 'POST',
            body: formData
        }).then(response => {
            if (response.ok) {
                // Redirect to the /results page
                window.location.href = '/results';
            } else {
                return response.text();
            }
        }).then(data => {
            if (data) {
                console.log(data);
                // Handle server error response here
            }
        }).catch(error => {
            console.error('Error sending the video:', error);
        });
    };

    // Stop all video streams
    const video = document.getElementById('webcam');
    video.srcObject.getTracks().forEach(track => track.stop());
}



const uploadBox = document.querySelector('.upload-box');
uploadBox.addEventListener('dragover', (event) => {
    event.preventDefault();
    // Add styling to indicate drag is over this area
});

uploadBox.addEventListener('drop', (event) => {
    event.preventDefault();
    const files = event.dataTransfer.files;
    uploadFile(files);
});
function generateScript() {
    // This function will make a request to /generate_script endpoint and handle the response
    fetch('/generate_script')
    .then(response => response.text())
    .then(data => {
        // Assuming the endpoint returns the script text as a response
        document.querySelector('.text-area').value = data;
        showWebcam();
         // Pasting the text in the textarea
    })
    .catch(error => console.error('Error:', error));
}
