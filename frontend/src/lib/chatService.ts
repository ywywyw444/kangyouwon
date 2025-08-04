import api from './api'

export interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

export interface ApiResponse {
  message: string
  data?: any
  status: 'success' | 'error'
  timestamp: string
  requestId: string
}

export interface ChatRequest {
  message: string
  userId?: string
  sessionId?: string
}

export class ChatService {
  private static instance: ChatService
  private sessionId: string

  constructor() {
    this.sessionId = this.generateSessionId()
  }

  static getInstance(): ChatService {
    if (!ChatService.instance) {
      ChatService.instance = new ChatService()
    }
    return ChatService.instance
  }

  private generateSessionId(): string {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }

  async sendMessage(message: string): Promise<ApiResponse> {
    try {
      const request: ChatRequest = {
        message,
        sessionId: this.sessionId,
        userId: 'user_' + Date.now()
      }

      // 실제 API 호출 (현재는 시뮬레이션)
      const response = await this.simulateApiCall(request)
      return response
    } catch (error) {
      console.error('Chat API Error:', error)
      throw new Error('메시지 전송 중 오류가 발생했습니다.')
    }
  }

  private async simulateApiCall(request: ChatRequest): Promise<ApiResponse> {
    // 실제 API 호출을 시뮬레이션
    await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000))
    
    const response: ApiResponse = {
      message: "요청을 성공적으로 처리했습니다.",
      data: {
        input: request.message,
        processedAt: new Date().toISOString(),
        responseType: "json",
        sessionId: request.sessionId,
        userId: request.userId,
        content: {
          text: `안녕하세요! "${request.message}"에 대한 JSON 응답입니다.`,
          timestamp: new Date().toISOString(),
          userQuery: request.message,
          analysis: {
            sentiment: "positive",
            confidence: 0.95,
            keywords: request.message.split(' ').slice(0, 3),
            language: "ko"
          },
          suggestions: [
            "추가 질문이 있으시면 언제든 말씀해 주세요.",
            "더 자세한 정보를 원하시면 구체적으로 질문해 주세요."
          ]
        },
        metadata: {
          processingTime: Math.random() * 1000 + 500,
          model: "gpt-4o-simulated",
          tokens: Math.floor(Math.random() * 1000) + 100
        }
      },
      status: "success",
      timestamp: new Date().toISOString(),
      requestId: `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    }

    return response
  }

  // 실제 API 호출을 위한 메서드 (향후 구현)
  async callRealApi(request: ChatRequest): Promise<ApiResponse> {
    try {
      const response = await api.post('/chat', request)
      return response.data
    } catch (error) {
      console.error('Real API Error:', error)
      throw error
    }
  }

  getSessionId(): string {
    return this.sessionId
  }

  resetSession(): void {
    this.sessionId = this.generateSessionId()
  }
}

export default ChatService.getInstance() 