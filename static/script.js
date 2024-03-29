document.addEventListener('DOMContentLoaded', function() {
  const loginForm = document.getElementById('login-form');
  const signupLink = document.getElementById('signup-link');
  const signupForm = document.getElementById('signup-form');
  const loginLink = document.getElementById('login-link');
  
  signupLink.addEventListener('click', function(e) {
    e.preventDefault();
    loginForm.classList.add('hidden');
    signupForm.classList.remove('hidden');
  });
  loginLink.addEventListener('click', function(e) {
    e.preventDefault();
    signupForm.classList.add('hidden');
    loginForm.classList.remove('hidden');
  });
});

document.addEventListener('DOMContentLoaded', function() {
  const ctx = document.getElementById('analytics-chart').getContext('2d');
  const chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
      datasets: [{
        label: 'Revenue',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
        data: [2000, 3000, 2500, 4000, 3500, 2800, 3200]
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
});