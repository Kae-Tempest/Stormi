import { useState } from 'react'
import { Subscribe } from './type.ts'
export default function App() {
  const [subscribe, setSubscribe] = useState<Subscribe>()
  const [eventType, setEventType] = useState('')
  const ws = new WebSocket('ws://127.0.0.1:8000/ws')

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data)
    setEventType(data[1])
    if (eventType || data[1] == 'channel.subscribe') {
      setSubscribe(JSON.parse(data[0]))
      console.log(subscribe)
    }
  }

  return (
    <>
      <div className='test'>{ subscribe?.user_name }</div>
      <div>{ eventType }</div>
    </>
  )
} 