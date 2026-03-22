# 📋 Sistema de Vistorias Prediais - PJI110 - A2026S1N1 - Grupo 22 (UNIVESP)

Sistema desenvolvido para automação de vistorias técnicas, com armazenamento em nuvem e autenticação dinâmica.

## 🚀 Tecnologias Utilizadas
* **Backend:** Python / Flask
* **Banco de Dados:** Oracle Cloud (SODA - JSON Document Store)
* **Hospedagem de Imagens:** API ImgBB
* **Frontend:** HTML5, CSS3, JavaScript (Jinja2)
* **Analytics:** Vercel Web Analytics

## 🛠️ Funcionalidades
* **Login Dinâmico:** Autenticação via banco de dados Oracle.
* **Cadastro de Vistoria:** Registro detalhado com upload de fotos.
* **Relatórios:** Visualização dinâmica das inspeções realizadas.
* **Fuso Horário:** Registro automático no horário de Brasília (UTC-3).

## 🔧 Como rodar o projeto
1. Instale as dependências Python:
   ```bash
   pip install -r requirements.txt
   ```

2. Instale as dependências Node.js (para analytics):
   ```bash
   npm install
   ```

3. Construa o bundle do analytics:
   ```bash
   npm run build
   ```

4. Execute a aplicação:
   ```bash
   python app.py
   ```

## 📊 Vercel Web Analytics
Este projeto inclui Vercel Web Analytics para rastreamento de visitantes e insights de tráfego.

### Como funciona
* O script analytics é automaticamente carregado em todas as páginas
* Os dados são enviados apenas quando a aplicação está hospedada no Vercel
* Modo de produção está configurado para otimizar a coleta de dados

### Reconstruir o Analytics Bundle
Se você modificar a configuração do analytics em `src/analytics.js`, execute:
```bash
npm run build
```
