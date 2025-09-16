import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, TouchableOpacity, Alert, ScrollView, Dimensions, Platform } from 'react-native';
import { useState, useEffect } from 'react';

const { width, height } = Dimensions.get('window');
const isWeb = Platform.OS === 'web';

export default function App() {
  const [gameStarted, setGameStarted] = useState(false);
  const [currentScene, setCurrentScene] = useState('inicio');
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [audioEnabled, setAudioEnabled] = useState(false);

  // Configurar PWA e fullscreen
  useEffect(() => {
    if (isWeb) {
      // Detectar se está em modo standalone (PWA instalado)
      const isStandalone = window.matchMedia('(display-mode: standalone)').matches;
      setIsFullscreen(isStandalone);

      // Adicionar evento de instalação PWA
      window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        // Mostrar botão customizado para instalar
      });

      // Configurar áudio
      const enableAudio = () => {
        setAudioEnabled(true);
        document.removeEventListener('click', enableAudio);
        document.removeEventListener('touchstart', enableAudio);
      };

      document.addEventListener('click', enableAudio);
      document.addEventListener('touchstart', enableAudio);

      return () => {
        document.removeEventListener('click', enableAudio);
        document.removeEventListener('touchstart', enableAudio);
      };
    }
  }, []);

  const enterFullscreen = () => {
    if (isWeb && document.documentElement.requestFullscreen) {
      document.documentElement.requestFullscreen().then(() => {
        setIsFullscreen(true);
      }).catch(console.error);
    }
  };

  const playAudio = (soundType: string) => {
    if (isWeb && audioEnabled) {
      // Criar áudio baseado no contexto
      const audio = new Audio();

      switch (soundType) {
        case 'click':
          // Som de clique suave
          audio.src = 'data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmgfBD+X2u27eCoEJIPK9N+LOR0PUrHl8R0QDIl2QAWDZzf9fgL9u3qwOtSF/4Y+3Q==';
          break;
        case 'success':
          // Som de sucesso
          audio.src = 'data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmgfBD+X2u27eCoEJIPK9N+LOR0PUrHl8R0QDIl2QAWDZzf9fgL9u3qwOtSF/4Y+3Q==';
          break;
        default:
          return;
      }

      audio.volume = 0.3;
      audio.play().catch(() => {});
    }
  };

  const startGame = () => {
    playAudio('success');
    setGameStarted(true);
    setCurrentScene('investigacao');
    if (!isFullscreen && isWeb) {
      enterFullscreen();
    }
    Alert.alert('Jogo Iniciado!', 'Bem-vindo ao Jogo de Investigação Mobile');
  };

  const renderScene = () => {
    switch (currentScene) {
      case 'investigacao':
        return (
          <ScrollView style={styles.sceneContainer}>
            <Text style={styles.sceneTitle}>🕵️ Investigação em Andamento</Text>
            <Text style={styles.sceneText}>
              Helena desapareceu no Solar dos Campos. Você é o detetive responsável por encontrá-la.
            </Text>
            <Text style={styles.sceneText}>
              • Interrogue os suspeitos{'\n'}
              • Colete evidências{'\n'}
              • Descubra a verdade
            </Text>

            <TouchableOpacity style={styles.actionButton} onPress={() => { playAudio('click'); setCurrentScene('personagens'); }}>
              <Text style={styles.buttonText}>Ver Personagens</Text>
            </TouchableOpacity>

            <TouchableOpacity style={styles.actionButton} onPress={() => { playAudio('click'); setCurrentScene('evidencias'); }}>
              <Text style={styles.buttonText}>Verificar Evidências</Text>
            </TouchableOpacity>
          </ScrollView>
        );

      case 'personagens':
        return (
          <ScrollView style={styles.sceneContainer}>
            <Text style={styles.sceneTitle}>👥 Personagens</Text>

            <View style={styles.characterCard}>
              <Text style={styles.characterName}>🧑‍💼 Dr. Marcus Valerius</Text>
              <Text style={styles.characterDesc}>Médico da família, nervoso e defensivo</Text>
            </View>

            <View style={styles.characterCard}>
              <Text style={styles.characterName}>👩‍🍳 Rosa Mendes</Text>
              <Text style={styles.characterDesc}>Cozinheira, conhece todos os segredos</Text>
            </View>

            <View style={styles.characterCard}>
              <Text style={styles.characterName}>👨‍💼 Sr. Antonio Campos</Text>
              <Text style={styles.characterDesc}>Pai de Helena, esconde algo</Text>
            </View>

            <TouchableOpacity style={styles.backButton} onPress={() => { playAudio('click'); setCurrentScene('investigacao'); }}>
              <Text style={styles.buttonText}>← Voltar</Text>
            </TouchableOpacity>
          </ScrollView>
        );

      case 'evidencias':
        return (
          <ScrollView style={styles.sceneContainer}>
            <Text style={styles.sceneTitle}>🔍 Evidências</Text>

            <View style={styles.evidenceCard}>
              <Text style={styles.evidenceTitle}>📱 Celular de Helena</Text>
              <Text style={styles.evidenceDesc}>Última mensagem às 22:30</Text>
            </View>

            <View style={styles.evidenceCard}>
              <Text style={styles.evidenceTitle}>🩸 Mancha de Sangue</Text>
              <Text style={styles.evidenceDesc}>Encontrada na escada do porão</Text>
            </View>

            <View style={styles.evidenceCard}>
              <Text style={styles.evidenceTitle}>🔑 Chave Misteriosa</Text>
              <Text style={styles.evidenceDesc}>Não pertence a nenhuma porta conhecida</Text>
            </View>

            <TouchableOpacity style={styles.backButton} onPress={() => { playAudio('click'); setCurrentScene('investigacao'); }}>
              <Text style={styles.buttonText}>← Voltar</Text>
            </TouchableOpacity>
          </ScrollView>
        );

      default:
        return null;
    }
  };

  if (!gameStarted) {
    return (
      <View style={styles.container}>
        <Text style={styles.title}>🔍 Jogo de Investigação</Text>
        <Text style={styles.subtitle}>Versão Mobile - Expo Go</Text>

        <View style={styles.welcomeContainer}>
          <Text style={styles.welcomeText}>
            Bem-vindo ao mistério do Solar dos Campos.{'\n\n'}
            Helena desapareceu e você é o único que pode encontrá-la.
          </Text>
        </View>

        <TouchableOpacity style={styles.startButton} onPress={startGame}>
          <Text style={styles.startButtonText}>🎮 Iniciar Jogo</Text>
        </TouchableOpacity>

        {isWeb && !isFullscreen && (
          <TouchableOpacity style={styles.fullscreenButton} onPress={enterFullscreen}>
            <Text style={styles.buttonText}>🔲 Tela Cheia</Text>
          </TouchableOpacity>
        )}

        <StatusBar style="light" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {renderScene()}
      <StatusBar style="light" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a2e',
    alignItems: 'center',
    justifyContent: 'center',
    padding: isWeb ? Math.min(width * 0.1, 50) : 20,
    minHeight: isWeb ? height : 'auto',
  },
  title: {
    fontSize: isWeb ? Math.min(width * 0.08, 48) : 28,
    fontWeight: 'bold',
    color: '#eee',
    marginBottom: 10,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: isWeb ? Math.min(width * 0.03, 20) : 16,
    color: '#bbb',
    marginBottom: 30,
    textAlign: 'center',
  },
  welcomeContainer: {
    marginBottom: 40,
    padding: 20,
    backgroundColor: '#16213e',
    borderRadius: 15,
    width: isWeb ? Math.min(width * 0.6, 600) : width - 40,
    maxWidth: 600,
  },
  welcomeText: {
    fontSize: isWeb ? Math.min(width * 0.025, 18) : 16,
    color: '#ddd',
    textAlign: 'center',
    lineHeight: 24,
  },
  startButton: {
    backgroundColor: '#d32f2f',
    padding: 20,
    borderRadius: 15,
    width: isWeb ? Math.min(width * 0.3, 300) : 200,
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    cursor: isWeb ? 'pointer' : 'default',
  },
  startButtonText: {
    color: '#fff',
    fontSize: isWeb ? Math.min(width * 0.03, 20) : 18,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  fullscreenButton: {
    backgroundColor: '#333',
    padding: 15,
    borderRadius: 10,
    marginTop: 15,
    width: isWeb ? Math.min(width * 0.25, 250) : 150,
    cursor: isWeb ? 'pointer' : 'default',
  },
  sceneContainer: {
    flex: 1,
    padding: isWeb ? Math.min(width * 0.05, 40) : 20,
    backgroundColor: '#1a1a2e',
    width: '100%',
    maxWidth: isWeb ? 800 : '100%',
    alignSelf: 'center',
  },
  sceneTitle: {
    fontSize: isWeb ? Math.min(width * 0.04, 32) : 24,
    fontWeight: 'bold',
    color: '#eee',
    marginBottom: 20,
    textAlign: 'center',
  },
  sceneText: {
    fontSize: isWeb ? Math.min(width * 0.025, 18) : 16,
    color: '#ddd',
    marginBottom: 20,
    lineHeight: 24,
  },
  actionButton: {
    backgroundColor: '#0f3460',
    padding: 15,
    borderRadius: 10,
    marginBottom: 15,
    cursor: isWeb ? 'pointer' : 'default',
  },
  backButton: {
    backgroundColor: '#444',
    padding: 15,
    borderRadius: 10,
    marginTop: 20,
    cursor: isWeb ? 'pointer' : 'default',
  },
  buttonText: {
    color: '#fff',
    fontSize: isWeb ? Math.min(width * 0.025, 18) : 16,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  characterCard: {
    backgroundColor: '#16213e',
    padding: 15,
    borderRadius: 10,
    marginBottom: 15,
    borderLeftWidth: 4,
    borderLeftColor: '#d32f2f',
    cursor: isWeb ? 'pointer' : 'default',
  },
  characterName: {
    fontSize: isWeb ? Math.min(width * 0.03, 20) : 18,
    fontWeight: 'bold',
    color: '#eee',
    marginBottom: 5,
  },
  characterDesc: {
    fontSize: isWeb ? Math.min(width * 0.02, 16) : 14,
    color: '#bbb',
  },
  evidenceCard: {
    backgroundColor: '#2a2a3e',
    padding: 15,
    borderRadius: 10,
    marginBottom: 15,
    borderLeftWidth: 4,
    borderLeftColor: '#ffa000',
    cursor: isWeb ? 'pointer' : 'default',
  },
  evidenceTitle: {
    fontSize: isWeb ? Math.min(width * 0.025, 18) : 16,
    fontWeight: 'bold',
    color: '#eee',
    marginBottom: 5,
  },
  evidenceDesc: {
    fontSize: isWeb ? Math.min(width * 0.02, 16) : 14,
    color: '#bbb',
  },
});
