document.addEventListener('DOMContentLoaded', function() {
    // Function to create price trend charts
    window.createPriceChart = function(productId, productName, dates, prices) {
        const ctx = document.getElementById(`chart-${productId}`);
        
        if (!ctx) return;
        
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: `Price per kg (₹)`,
                    data: prices,
                    backgroundColor: 'rgba(46, 125, 50, 0.2)',
                    borderColor: 'rgba(46, 125, 50, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(46, 125, 50, 1)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgba(46, 125, 50, 1)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            title: function(tooltipItems) {
                                return productName;
                            },
                            label: function(context) {
                                return `₹${context.parsed.y.toFixed(2)} per kg on ${context.label}`;
                            }
                        }
                    },
                    title: {
                        display: true,
                        text: productName,
                        font: {
                            size: 16
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        },
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        beginAtZero: false,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        },
                        title: {
                            display: true,
                            text: 'Price per kg (₹)'
                        },
                        ticks: {
                            callback: function(value) {
                                return '₹' + value.toFixed(2);
                            }
                        }
                    }
                }
            }
        });
        
        return chart;
    };
    
    // Function to create average price chart for Daily Mandi
    window.createAveragePriceChart = function(categories, avgPrices) {
        const ctx = document.getElementById('average-price-chart');
        
        if (!ctx) return;
        
        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: categories,
                datasets: [{
                    label: 'Average Price per kg (₹)',
                    data: avgPrices,
                    backgroundColor: 'rgba(255, 143, 0, 0.7)',
                    borderColor: 'rgba(255, 143, 0, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    title: {
                        display: true,
                        text: 'Average Prices by Category',
                        font: {
                            size: 16
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        },
                        ticks: {
                            callback: function(value) {
                                return '₹' + value.toFixed(2);
                            }
                        }
                    }
                }
            }
        });
        
        return chart;
    };
    
    // Function to create a rating distribution chart
    window.createRatingChart = function(ratings) {
        const ctx = document.getElementById('rating-distribution-chart');
        
        if (!ctx) return;
        
        // Count ratings
        const ratingCounts = [0, 0, 0, 0, 0]; // 1 to 5 stars
        
        ratings.forEach(rating => {
            ratingCounts[rating - 1]++;
        });
        
        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars'],
                datasets: [{
                    label: 'Number of Ratings',
                    data: ratingCounts,
                    backgroundColor: [
                        'rgba(211, 47, 47, 0.7)',
                        'rgba(255, 143, 0, 0.7)',
                        'rgba(255, 193, 7, 0.7)',
                        'rgba(76, 175, 80, 0.7)',
                        'rgba(46, 125, 50, 0.7)'
                    ],
                    borderColor: [
                        'rgba(211, 47, 47, 1)',
                        'rgba(255, 143, 0, 1)',
                        'rgba(255, 193, 7, 1)',
                        'rgba(76, 175, 80, 1)',
                        'rgba(46, 125, 50, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Rating Distribution',
                        font: {
                            size: 16
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        },
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });
        
        return chart;
    };
    
    // Calculate and display monthly trend
    window.createMonthlyTrendChart = function(productData) {
        const ctx = document.getElementById('monthly-trend-chart');
        
        if (!ctx || !productData || productData.length === 0) return;
        
        // Process data to get monthly averages
        const monthlyData = {};
        
        productData.forEach(product => {
            if (!product.dates || !product.prices || product.dates.length === 0) return;
            
            for (let i = 0; i < product.dates.length; i++) {
                const date = new Date(product.dates[i]);
                const monthYear = `${date.getFullYear()}-${date.getMonth() + 1}`;
                
                if (!monthlyData[monthYear]) {
                    monthlyData[monthYear] = {
                        total: 0,
                        count: 0,
                        month: date.toLocaleString('default', { month: 'short' }),
                        year: date.getFullYear()
                    };
                }
                
                monthlyData[monthYear].total += product.prices[i];
                monthlyData[monthYear].count++;
            }
        });
        
        // Convert to arrays for chart
        const months = [];
        const avgPrices = [];
        
        // Sort months chronologically
        Object.keys(monthlyData)
            .sort()
            .forEach(key => {
                const data = monthlyData[key];
                months.push(`${data.month} ${data.year}`);
                avgPrices.push(data.total / data.count);
            });
        
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: months,
                datasets: [{
                    label: 'Average Price per kg (₹)',
                    data: avgPrices,
                    backgroundColor: 'rgba(25, 118, 210, 0.2)',
                    borderColor: 'rgba(25, 118, 210, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(25, 118, 210, 1)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgba(25, 118, 210, 1)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    title: {
                        display: true,
                        text: 'Monthly Price Trend',
                        font: {
                            size: 16
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        beginAtZero: false,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        },
                        ticks: {
                            callback: function(value) {
                                return '₹' + value.toFixed(2);
                            }
                        }
                    }
                }
            }
        });
        
        return chart;
    };
});
