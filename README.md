Much of this code came from: https://fastapi.tiangolo.com/advanced/websockets/
source of project ::: --->>> https://youtu.be/ADVsjLHevtY?si=rf8E-7bh9fLXR4Rr




explaination 
1. Frontend → Backend: Data kaise ja raha hai?

Tere HTML/JS me ye line hai:

ws.send(input.value)


Matlab jab user send button dabata hai, jo bhi message input box me likha hai, wo WebSocket connection ke through backend ko bhej diya jata hai.

Ye message backend me yahaan receive hota hai:

data = await websocket.receive_text()


Iska matlab: data variable ke andar frontend se bheja gaya text message aa gaya.

2. Backend → Message broadcast kaise ho raha hai?

Jab backend ko message milta hai, ye do kaam karta hai:

Personal reply bhejta hai (sirf usi user ko jisne bheja):

await manager.send_personal_message(f"You wrote: {data}", websocket)


→ Tere browser me dikhega You wrote: <message>.

Broadcast (sabhi users ko bhejta hai):

await manager.broadcast(f"Client #{client_id} says: {data}")


→ Jo bhi connected users hai (apna bhi aur dusre bhi), un sabko ye message dikhega.

3. Ek user dusre ka message kaise dekh raha hai?

Jab Client #101 message bhejta hai "Hello", backend sabhi active connections me ye bhej deta hai:

Client #101 says: Hello


Ab suppose 2 users connected hai:

Client #101

Client #102

Dono ke frontend JS me ye line hai:

ws.onmessage = function(event) {
    var message = document.createElement('li');
    message.textContent = event.data;
    messages.appendChild(message);
};


Matlab backend se jo bhi data aaya (event.data), wo chat box me append ho jaata hai.

Isliye agar Client #101 likhta hai "Hello", to Client #102 ke browser me bhi "Client #101 says: Hello" show hoga.

✅ Summary in Hinglish:

User jab type karta hai aur send karta hai → ws.send() ke through message backend ko jaata hai.

Backend receive_text() se message le leta hai.

Backend broadcast() karke wo message sabhi connected clients ko bhej deta hai.

Har client ka frontend onmessage event pe wo text chat box me add kar deta hai → isliye sab ek dusre ke messages dekh pate hain.
