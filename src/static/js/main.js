async function carregarGrafico() {
    // Busca os dados da rota /leituras com o parâmetro json [cite: 140, 141]
    const res = await fetch('/leituras?formato=json');
    const dados = await res.json();
    
    // Pega as últimas 10 leituras e inverte para ordem cronológica [cite: 141, 185]
    const ultimos = dados.slice(0, 10).reverse();
    
    const labels = ultimos.map(l => l.timestamp.split(' ')[1]); // Pega apenas a hora
    const temps = ultimos.map(l => l.temperatura);
    const umids = ultimos.map(l => l.umidade);

    const ctx = document.getElementById('graficoTemporal').getContext('2d');
    
    // Destrói gráfico anterior se existir para evitar sobreposição ao atualizar
    if (window.meuGrafico) {
        window.meuGrafico.destroy();
    }

    window.meuGrafico = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Temperatura (°C)',
                    data: temps,
                    borderColor: 'rgb(255, 99, 132)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    tension: 0.3,
                    yAxisID: 'y'
                },
                {
                    label: 'Umidade (%)',
                    data: umids,
                    borderColor: 'rgb(54, 162, 235)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    tension: 0.3,
                    yAxisID: 'y1' // Eixo secundário opcional para escalas diferentes
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: { display: true, text: 'Temperatura (°C)' }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: { display: true, text: 'Umidade (%)' },
                    grid: { drawOnChartArea: false } // Evita poluição de linhas
                }
            }
        }
    });

    // Atualiza os indicadores visuais no dashboard [cite: 186, 187]
    if (ultimos.length > 0) {
        const ultima = ultimos[ultimos.length - 1];
        document.getElementById('temp-val').innerText = ultima.temperatura;
        document.getElementById('umid-val').innerText = ultima.umidade;
    }
}

// Carrega o gráfico inicialmente
carregarGrafico();

// Atualiza automaticamente a cada 10 segundos para efeito de tempo real 
setInterval(carregarGrafico, 10000);