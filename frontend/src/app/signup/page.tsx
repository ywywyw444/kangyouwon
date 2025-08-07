'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import axios from 'axios'

export default function SignupPage() {
  const router = useRouter()
  const [userData, setUserData] = useState({
    industry: '',
    email: '',
    name: '',
    age: '',
    auth_id: '',
    auth_pw: ''
  })
  const [isLoading, setIsLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [confirmPassword, setConfirmPassword] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    // 비밀번호 확인
    if (userData.auth_pw !== confirmPassword) {
      alert('비밀번호가 일치하지 않습니다.')
      setIsLoading(false)
      return
    }

    // 이벤트 데이터를 JSON 형태로 alert 창에 표시
    const eventData = {
      industry: userData.industry,
      email: userData.email,
      name: userData.name,
      age: userData.age,
      auth_id: userData.auth_id,
      auth_pw: userData.auth_pw
    }

    alert(`이벤트 데이터:\n${JSON.stringify(eventData, null, 2)}`)

    try {
      // Gateway API로 회원가입 요청
      const response = await axios.post('http://localhost:8080/signup', userData, {
        headers: {
          'Content-Type': 'application/json',
        }
      })

      // axios는 성공 시 자동으로 response.data를 반환
      const result = response.data

      // 회원가입 성공
      alert(`회원가입 성공!\n사용자: ${result.user.name}`)
      // 회원가입 성공 시 로그인 페이지로 이동
      router.push('/')
    } catch (error) {
      // axios 에러 처리
      if (axios.isAxiosError(error)) {
        if (error.response) {
          // 서버에서 오류 응답을 받은 경우
          const errorMessage = error.response.data?.error || '알 수 없는 오류가 발생했습니다.'
          alert(`회원가입 실패: ${errorMessage}`)
        } else if (error.request) {
          // 요청은 보냈지만 응답을 받지 못한 경우
          alert('서버에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.')
        } else {
          // 요청 설정 중 오류가 발생한 경우
          alert(`요청 오류: ${error.message}`)
        }
      } else {
        // 기타 오류
        alert(`연결 오류: ${error instanceof Error ? error.message : '알 수 없는 오류가 발생했습니다.'}`)
      }
    } finally {
      setIsLoading(false)
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setUserData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="max-w-md w-full space-y-8">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          {/* 헤더 */}
          <div className="text-center mb-8">
            <div className="mx-auto h-12 w-12 bg-green-600 rounded-full flex items-center justify-center mb-4">
              <svg className="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
              </svg>
            </div>
            <h2 className="text-3xl font-bold text-gray-900 mb-2">회원가입</h2>
            <p className="text-gray-600">새 계정을 만드세요</p>
          </div>

          {/* 회원가입 폼 */}
          <form className="space-y-6" onSubmit={handleSubmit}>
            {/* 업종 선택 */}
            <div>
              <label htmlFor="industry" className="block text-sm font-medium text-gray-700 mb-2">
                업종 <span className="text-red-500">*</span>
              </label>
              <select
                id="industry"
                name="industry"
                required
                value={userData.industry}
                onChange={handleInputChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-colors text-gray-900"
              >
                <option value="">업종을 선택하세요</option>
                <option value="제조업">제조업</option>
                <option value="서비스업">서비스업</option>
                <option value="IT/소프트웨어">IT/소프트웨어</option>
                <option value="금융업">금융업</option>
                <option value="건설업">건설업</option>
                <option value="유통업">유통업</option>
                <option value="의료/제약">의료/제약</option>
                <option value="에너지">에너지</option>
                <option value="기타">기타</option>
              </select>
            </div>

            {/* 이메일 */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                이메일
              </label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                value={userData.email}
                onChange={handleInputChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-colors text-gray-900"
                placeholder="example@company.com"
              />
            </div>

            {/* 이름 */}
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
                이름
              </label>
              <input
                id="name"
                name="name"
                type="text"
                autoComplete="name"
                value={userData.name}
                onChange={handleInputChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-colors text-gray-900"
                placeholder="홍길동"
              />
            </div>

            {/* 나이 */}
            <div>
              <label htmlFor="age" className="block text-sm font-medium text-gray-700 mb-2">
                나이
              </label>
              <input
                id="age"
                name="age"
                type="number"
                min="1"
                max="120"
                value={userData.age}
                onChange={handleInputChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-colors text-gray-900"
                placeholder="30"
              />
            </div>

            {/* 아이디 */}
            <div>
              <label htmlFor="auth_id" className="block text-sm font-medium text-gray-700 mb-2">
                아이디
              </label>
              <input
                id="auth_id"
                name="auth_id"
                type="text"
                autoComplete="username"
                value={userData.auth_id}
                onChange={handleInputChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-colors text-gray-900"
                placeholder="사용할 아이디를 입력하세요"
              />
            </div>

            {/* 비밀번호 */}
            <div>
              <label htmlFor="auth_pw" className="block text-sm font-medium text-gray-700 mb-2">
                비밀번호
              </label>
              <div className="relative">
                <input
                  id="auth_pw"
                  name="auth_pw"
                  type={showPassword ? "text" : "password"}
                  autoComplete="new-password"
                  required
                  value={userData.auth_pw}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-colors text-gray-900"
                  placeholder="••••••••"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                >
                  {showPassword ? (
                    <svg className="h-5 w-5 text-gray-400 hover:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21" />
                    </svg>
                  ) : (
                    <svg className="h-5 w-5 text-gray-400 hover:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  )}
                </button>
              </div>
            </div>

            {/* 비밀번호 확인 */}
            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-2">
                비밀번호 확인
              </label>
              <div className="relative">
                <input
                  id="confirmPassword"
                  name="confirmPassword"
                  type={showConfirmPassword ? "text" : "password"}
                  autoComplete="new-password"
                  required
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-colors text-gray-900"
                  placeholder="••••••••"
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                >
                  {showConfirmPassword ? (
                    <svg className="h-5 w-5 text-gray-400 hover:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21" />
                    </svg>
                  ) : (
                    <svg className="h-5 w-5 text-gray-400 hover:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  )}
                </button>
              </div>
            </div>

            <div>
              <button
                type="submit"
                disabled={isLoading}
                className="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {isLoading ? (
                  <div className="flex items-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    회원가입 중...
                  </div>
                ) : (
                  '회원가입'
                )}
              </button>
            </div>

            <div className="text-center">
              <p className="text-sm text-gray-600">
                이미 계정이 있으신가요?{' '}
                <a href="/" className="font-medium text-green-600 hover:text-green-500 transition-colors">
                  로그인
                </a>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}
