'use client'

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-100 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <div className="text-center mb-8">
            <div className="mx-auto h-16 w-16 bg-green-600 rounded-full flex items-center justify-center mb-4">
              <svg className="h-8 w-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h1 className="text-4xl font-bold text-gray-900 mb-2">로그인 성공!</h1>
            <p className="text-gray-600 text-lg">대시보드에 오신 것을 환영합니다</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-blue-50 p-6 rounded-xl">
              <h3 className="text-xl font-semibold text-blue-900 mb-2">사용자 정보</h3>
              <p className="text-blue-700">로그인된 사용자 정보가 여기에 표시됩니다.</p>
            </div>
            
            <div className="bg-green-50 p-6 rounded-xl">
              <h3 className="text-xl font-semibold text-green-900 mb-2">최근 활동</h3>
              <p className="text-green-700">최근 로그인 기록과 활동 내역을 확인하세요.</p>
            </div>
            
            <div className="bg-purple-50 p-6 rounded-xl">
              <h3 className="text-xl font-semibold text-purple-900 mb-2">설정</h3>
              <p className="text-purple-700">계정 설정 및 개인정보를 관리하세요.</p>
            </div>
          </div>
          
          <div className="mt-8 text-center">
            <button 
              onClick={() => window.history.back()}
              className="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
            >
              로그인 페이지로 돌아가기
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
