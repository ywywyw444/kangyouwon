import { create } from 'zustand'

interface Todo {
  id: number
  text: string
  completed: boolean
}

interface Store {
  count: number
  todos: string[]
  increment: () => void
  decrement: () => void
  addTodo: (text: string) => void
  removeTodo: (index: number) => void
}

export const useStore = create<Store>((set) => ({
  count: 0,
  todos: [],
  
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  
  addTodo: (text: string) => 
    set((state) => ({ todos: [...state.todos, text] })),
  
  removeTodo: (index: number) =>
    set((state) => ({
      todos: state.todos.filter((_, i) => i !== index)
    })),
})) 