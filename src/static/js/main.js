async function carregarGrafico() {
    const res = await fetch('/leituras?formato=json');
    const dados = await res.json();
    
    // Inverter para mostrar da mais antiga para a mais nova no gráfico
    const ultimos = dados.slice(0, 10).reverse();
    
    const labels = ultimos.map(l => l.timestamp.split(' ')[1]);
    const temps = ultimos.map(l => l.temperatura);

    const ctx = document.getElementById('graficoTemporal').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Temperatura (°C)',
                data: temps,
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.1
            }]
        }
    });

    if (ultimos.length > 0) {
        document.getElementById('temp-val').innerText = ultimos[ultimos.length-1].temperatura;
        document.getElementById('umid-val').innerText = ultimos[ultimos.length-1].umidade;
    }
}

carregarGrafico();