document.addEventListener("DOMContentLoaded", function () {
  const fileInput = document.getElementById("image-upload");
  const preview = document.getElementById("image-preview");
  const resultDiv = document.getElementById("result");
  const predictBtn = document.getElementById("predict-btn");

  // Default chart values
  const ctx = document.getElementById("confidence-chart").getContext("2d");
  const defaultScores = Array(10).fill(0.1);

  const chartInstance = new Chart(ctx, {
  type: "bar",
  data: {
    labels: ["Digit 0", "Digit 1", "Digit 2", "Digit 3", "Digit 4", "Digit 5", "Digit 6", "Digit 7", "Digit 8", "Digit 9"],
    datasets: [{
      label: "Confidence Score",
      data: defaultScores,
      backgroundColor: "rgba(75, 192, 192, 0.6)",
      borderColor: "rgba(75, 192, 192, 1)",
      borderWidth: 2
    }]
  },
  options: {
  layout: {
    padding: {
      top: 30,
      bottom: 10
    }
  },
    plugins: {
    legend: {
      display: true,
      labels: {
        padding: 20
      }
    },
    datalabels: {
        anchor: 'start',
        align: 'center',
        color: '#000',
        font: {
          size: 5,
          weight: 'small'
        },
        formatter: function(value) {
          return value.toFixed(2);
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 1
      }
    }
  },
  plugins: [ChartDataLabels]
});

  // Upload preview
  fileInput.addEventListener("change", function () {
    const file = fileInput.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        preview.src = e.target.result;
        preview.style.display = "block";
      };
      reader.readAsDataURL(file);
    } else {
      preview.style.display = "none";
    }
  });

  // Predict from uploaded image
  predictBtn.addEventListener("click", async function () {
    const file = fileInput.files[0];
    if (!file) {
      alert("Please upload an image.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("/predict", {
        method: "POST",
        body: formData
      });

      const data = await response.json();

      if (data.error) {
        resultDiv.innerHTML = `<span style="color:red;">${data.error}</span>`;
        return;
      }

      resultDiv.innerHTML = `<strong>Predicted Digit:</strong> ${data.predicted_digit}`;
      chartInstance.data.datasets[0].data = data.confidence_scores;
      chartInstance.update();

    } catch (err) {
      resultDiv.innerHTML = `<span style="color:red;">Error: ${err.message}</span>`;
    }
  });

  // Predict from per-card button
  document.querySelectorAll(".predict-sample-btn").forEach(button => {
    button.addEventListener("click", async function () {
      const card = this.closest(".example-card");
      const imageUrl = card.querySelector("img").dataset.src;

      try {
        const response = await fetch(imageUrl);
        const blob = await response.blob();
        const formData = new FormData();
        formData.append("file", blob, "sample.jpg");

        const predictResponse = await fetch("/predict", {
          method: "POST",
          body: formData
        });

        const data = await predictResponse.json();

        if (data.error) {
          resultDiv.innerHTML = `<span style="color:red;">${data.error}</span>`;
          return;
        }

        resultDiv.innerHTML = `<strong>Predicted Digit:</strong> ${data.predicted_digit}`;
        chartInstance.data.datasets[0].data = data.confidence_scores;
        chartInstance.update();

      } catch (err) {
        resultDiv.innerHTML = `<span style="color:red;">Error: ${err.message}</span>`;
      }
    });
  });
});
