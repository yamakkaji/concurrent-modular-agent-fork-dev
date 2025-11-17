import concurrent_modular_agent as cma
import time, cv2, base64, threading
from openai import OpenAI

default_prompt = """
Give a concise description of this image.
"""

def send_to_openai(frame, openai_client, agent, prompt):
    ok, buf = cv2.imencode('.jpg', frame)
    if not ok:
        return

    b64 = base64.b64encode(buf).decode('utf-8')

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    { "type": "text", "text": prompt },
                    {
                        "type": "image_url",
                        "image_url": { "url": f"data:image/jpeg;base64,{b64}" }
                    }
                ]
            }
        ],
        max_tokens=4000
    )

    vision_text = response.choices[0].message.content
    print(f'# vision: {vision_text}', flush=True)
    agent.state.add(vision_text)

def vision(device: str | int = 0, 
           prompt: str = default_prompt,
           show_window: bool = False):
    def vision_module(agent: cma.AgentInterface):
        openai_client = OpenAI()
        cap = cv2.VideoCapture(device)

        # 対応していればバッファサイズを1に（古いフレームを溜めない）
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        interval = 10.0  # 秒
        last_sent = 0.0

        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            # ここで常に最新フレームを表示（ほぼリアルタイム）
            if show_window:
                cv2.imshow('camera', frame)
                key = cv2.waitKey(1) & 0xFF
                if key == 27:  # ESCで終了
                    break

            now = time.time()
            if now - last_sent >= interval:
                last_sent = now
                # 送信用にコピーを取って別スレッドでOpenAIへ
                snapshot = frame.copy()
                threading.Thread(
                    target=send_to_openai,
                    args=(snapshot, openai_client, agent, prompt),
                    daemon=True
                ).start()

        cap.release()
        cv2.destroyAllWindows()
    return vision_module
