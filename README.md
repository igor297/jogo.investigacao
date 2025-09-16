# 🔍 Jogo de Investigação - Solar dos Campos

Um jogo de investigação completo com frontend React Native/Expo e backend Python Flask. Funciona como app mobile, PWA web e aplicação completa com IA.

## 🏗️ Arquitetura

- **Frontend**: React Native + Expo (PWA)
- **Backend**: Python Flask + SQLite + IA
- **Deploy**: Vercel (frontend) + Docker (fullstack)

## 🚀 Opções de Deploy

### Pré-requisitos
- Conta no [Vercel](https://vercel.com)
- Repositório no GitHub com este código

## 🐳 Deploy Completo (Frontend + Backend)

### Opção 1: Docker Compose (Recomendado)

```bash
# Clonar repositório
git clone https://github.com/igor297/jogo.investigacao.git
cd jogo.investigacao

# Build do frontend
npm install
npm run build

# Rodar com Docker
docker-compose up -d

# Acesso:
# Frontend: http://localhost:3000
# Backend: http://localhost:5000
```

### Opção 2: Desenvolvimento Local

```bash
# Backend Python
cd backend
pip install -r requirements.txt
python app.py

# Frontend (nova aba)
npm install
npm run web
```

## 🌐 Deploy Frontend Only (Vercel)

### 📋 Passos para Deploy

1. **Conectar ao GitHub**
   - Acesse [vercel.com](https://vercel.com)
   - Clique em "Import Project"
   - Conecte seu repositório GitHub

2. **Configurar o Projeto**
   - Selecione o repositório `jogo-investigacao-mobile`
   - Vercel detectará automaticamente as configurações

3. **Build Commands (Automático)**
   ```bash
   # Build command
   npm run vercel-build

   # Output directory
   web-build
   ```

4. **Deploy**
   - Clique em "Deploy"
   - Vercel fará o build automaticamente
   - URL estará disponível em poucos minutos

### 🔧 Configuração Manual (se necessário)

Se precisar configurar manualmente:

```json
{
  "buildCommand": "npm run vercel-build",
  "outputDirectory": "web-build",
  "devCommand": "npm run web",
  "installCommand": "npm install"
}
```

### 📱 Funcionalidades

- ✅ **PWA** - Instalável como app
- ✅ **Fullscreen** - Experiência imersiva
- ✅ **Áudio** - Sons de interface
- ✅ **Responsivo** - Mobile e desktop
- ✅ **Offline-first** - Funciona sem internet

### 🎮 Como Jogar

1. Acesse a URL do Vercel
2. Clique em "Tela Cheia" para melhor experiência
3. Inicie o jogo
4. Navegue entre personagens e evidências
5. Descubra o mistério de Helena!

### 🔗 URLs Após Deploy

- **Produção**: `https://seu-projeto.vercel.app`
- **Preview**: URLs automáticas para cada commit
- **Dashboard**: `https://vercel.com/dashboard`

### 📋 Comandos Disponíveis

```bash
# Desenvolvimento
npm start              # Expo Metro bundler
npm run web           # Expo web
npm run android       # Android (requer setup)
npm run ios           # iOS (requer setup)

# Build
npm run build         # Build para web
npm run vercel-build  # Build otimizado para Vercel
```

### 🎯 Otimizações Vercel

- **Tree Shaking** - Reduz bundle size
- **Fast Resolver** - Build mais rápido
- **Static Export** - Performance otimizada
- **SPA Routing** - Navegação correta

### 🐛 Troubleshooting

**Build falha?**
- Verifique se `expo export` funciona localmente
- Confirme dependências no `package.json`

**PWA não instala?**
- Verifique se `manifest.json` está acessível
- Confirme HTTPS (Vercel usa por padrão)

**Performance lenta?**
- Ative compressão no Vercel
- Verifique bundle size com `npm run build`

### 📞 Suporte

Criado com ❤️ usando:
- [Expo](https://expo.dev)
- [React Native](https://reactnative.dev)
- [Vercel](https://vercel.com)