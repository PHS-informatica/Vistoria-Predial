function abrirModal(dados) {
    const modal = document.getElementById("meuModal");
    const conteudo = document.getElementById("conteudoModal");
    
    // 1. Criamos a galeria de imagens APENAS se houver fotos válidas
    let fotosHtml = '';

    // Verificamos se existe a lista e se não é o placeholder
    if (Array.isArray(dados.url_fotos) && dados.url_fotos.length > 0 && dados.url_fotos[0] !== "https://via.placeholder.com/150") {
        
        // Colocamos TODA a estrutura da caixa azul dentro da variável
        fotosHtml = `
            <div style="margin-top:20px; padding: 15px; border: 2px dashed #3498db; border-radius: 12px; background-color: #f0f7ff;">
                <p style="margin-bottom: 10px; color: #2c3e50; font-weight: bold; font-size: 0.9em; text-align: center;">
                    📸 Evidências Fotográficas
                </p>
                <div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;">
                    ${dados.url_fotos.map(url => 
                        `<img src="${url}" 
                              style="width: 120px; height: 120px; object-fit: cover; border-radius: 8px; border: 2px solid #3498db; cursor: pointer; transition: transform 0.2s;" 
                              onmouseover="this.style.transform='scale(1.05)'" 
                              onmouseout="this.style.transform='scale(1)'"
                              onclick="window.open('${url}', '_blank')" 
                              title="Clique para ampliar">`
                    ).join('')}
                </div>
                <p style="font-size: 0.7em; color: #7f8c8d; margin-top: 10px; text-align: center;">
                    (Clique na foto para ampliar)
                </p>
            </div>
        `;
    }

    // 2. Montamos o modal (Note que agora ${fotosHtml} traz a caixa inteira ou nada)
    conteudo.innerHTML = `
        <h2 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; margin-top: 0;">
            ${dados.nome_predio}
        </h2>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 15px; font-size: 0.9em;">
            <div><strong>📍 Endereço:</strong><br> ${dados.endereco || 'N/A'}</div>
            <div><strong>👤 Vistoriador:</strong><br> ${dados.vistoriador}</div>
            <div><strong>📅 Data Vistoria:</strong><br> ${dados.data_vistoria}</div>
            <div><strong>⏳ Venc. Alvará:</strong><br> ${dados.alvara_vencimento}</div>
            <div><strong>⏭️ Próxima Vistoria:</strong><br> ${dados.proxima_vistoria || 'Não agendada'}</div>
        </div>

        <hr style="border: 0; border-top: 1px solid #eee; margin: 15px 0;">

        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; font-size: 0.85em;">
            <div><strong>🎨 Pintura:</strong><br> ${dados.pintura}</div>
            <div><strong>🧱 Fachada:</strong><br> ${dados.fachada}</div>
            <div><strong>👣 Piso:</strong><br> ${dados.piso}</div>
            <div><strong>⚡ Elétrica:</strong><br> ${dados.eletrica}</div>
            <div><strong>💧 Hidráulica:</strong><br> ${dados.hidraulica}</div>
            <div><strong>🏠 Cobertura:</strong><br> ${dados.cobertura}</div>
            <div><strong>🛡️ Segurança:</strong><br> ${dados.itens_seguranca}</div>
            <div><strong>🌪️ Ventilação:</strong><br> ${dados.sistema_ventilacao}</div>
            <div><strong>🏗️ Estrutura:</strong><br> ${dados.laudo_estrutural}</div>
        </div>

        <div style="background: #fdf6b2; padding: 12px; border-radius: 6px; margin-top: 15px; border-left: 4px solid #e3a008; font-size: 0.9em;">
            <strong>💡 Observações:</strong><br>
            <p style="margin: 5px 0 0 0;">${dados.observacao}</p>
        </div>
        
        ${fotosHtml} 
    `;
    modal.style.display = "block";
}

function fecharModal() {
    document.getElementById("meuModal").style.display = "none";
}

function excluirVistoria(key) {
    if (!key || key === "" || key === "None") {
        alert("Erro: Não foi possível identificar o ID desta vistoria no banco.");
        return;
    }

    if (confirm("Tem certeza que deseja excluir esta vistoria definitivamente?")) {
        fetch(`/excluir/${key}`, { 
            method: 'POST' 
        })
        .then(response => {
            if (!response.ok) throw new Error(`Erro no servidor: ${response.status}`);
            return response.json();
        })
        .then(data => {
            if (data.status === "sucesso") {
                alert("🗑️ Vistoria removida com sucesso!");
                window.location.reload();
            } else {
                alert("Erro ao excluir: " + data.mensagem);
            }
        })
        .catch(error => {
            console.error('Erro detalhado:', error);
            alert("Não foi possível excluir. Verifique a conexão.");
        });
    }
}

window.onclick = function(event) {
    const modal = document.getElementById("meuModal");
    if (event.target == modal) fecharModal();
}