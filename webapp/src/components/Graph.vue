<template>
    <div class="graph">
        TeST
    </div>
</template>

<script>
export default {
    
    mounted() {

        let socket = new WebSocket("ws://localhost:8000")

        console.log("TRYING TO CONNECT")

        socket.onmessage = message => {

            console.log("RECEIVED MESSAGE", message)
        }
    }
}
</script>