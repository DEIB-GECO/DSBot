<template>
  <div>
    <v-container fluid>
      <v-row>
        <v-col id="chat" flat class="chat-container">
          <v-row
            v-for="(item, index) in tuningChat"
            :key="index"
            :class="{ 'flex-row-reverse': !item.isBot }"
          >
            <v-col :cols="2">
              <font-awesome-icon
                :icon="item.isBot ? 'robot' : 'user'"
                size="2x"
                color="#424242"
              />
            </v-col>
            <v-col :cols="9">
              <v-card
                :color="item.isBot ? 'white' : 'accent'"
                class="py-1 px-2"
              >
                {{ item.message }}
              </v-card>
            </v-col>
          </v-row>
        </v-col>
      </v-row>

      <v-row dense>
        <v-col xl="10" lg="9" md="8" sm="7">
          <v-textarea
            v-model="utterance"
            solo
            flat
            no-resize
            label="Write here to chat"
            rows="3"
            background-color="grey lighten-3"
            hide-details="true"
            @keyup.enter="sendText"
          ></v-textarea>
        </v-col>

        <v-col cols="2" class="align-self-stretch">
          <v-btn
            height="100%"
            color="primary"
            :depressed="true"
            @click="sendText"
          >
            <font-awesome-icon icon="chevron-right" size="2x" color="white" />
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { mapActions, mapState, mapMutations } from 'vuex'
import io from 'socket.io-client'

const SOCKET_PATH = 'localhost'
const SOCKET_ENDPOINT = '/test'

const socket = io(SOCKET_ENDPOINT, {
  path: SOCKET_PATH,
  reconnection: true,
  reconnectionDelay: 500,
  reconnectionAttempts: 10,
})

export default {
  components: {},
  props: {
    destination: {
      type: String,
      default: 'mmcc',
    },
  },
  data() {
    return {
      utterance: '',
    }
  },
  computed: {
    ...mapState(['tuningChat']),
  },
  updated() {
    this.scrollToEnd()
  },
  created() {
    if (this.destination === 'refinement') {
      // socket.emit('ack', { message_id: this.lastMessageId, location: 'crated' })
      socket.on('message_response', (payload) => {
        if (payload.type) {
          console.log('server sent JSON_response', payload)
          this.receiveChat(payload.message)
        } else {
          console.log('ERRORE STRANO', payload)
        }
      })
      socket.on('reconnect', () => {
        socket.emit('ack', {
          message_id: this.lastMessageId,
          location: 'reconnect',
        })
        console.log('RECONNECT! Mando ack')
      })
      socket.on('wait_msg', (payload) => {
        console.log('Ehi wait msg', payload)
        this.jsonResponseParsingFunctions.message(payload.payload)
        this.setSendButtonStatus(false)
      })
    }
  },
  methods: {
    ...mapActions(['toFramework', 'sendChatMessage']),
    ...mapMutations(['sendChat', 'receiveChat']),
    sendText() {
      if (this.utterance.trim() !== '' && this.utterance !== '\n') {
        if (this.destination === 'mmcc') this.toFramework(this.utterance)
        else if (this.destination === 'comprehension') {
          this.sendChatMessage({
            destination: this.destination,
            message: this.utterance,
          })
        } else if (this.destination === 'refinement') {
          this.sendSocketMessage()
        }
        this.utterance = ''
      }
    },
    scrollToEnd() {
      const container = this.$el.querySelector('#chat')
      // console.log(container);
      if (container) {
        container.scrollTop = container.scrollHeight
      }
    },
    sendSocketMessage() {
      this.sendChat(this.utterance)
      socket.emit('message_sent', { message: this.utterance })
    },
  },
}
</script>

<style scoped>
.chat-container {
  height: 600px; /* This component is this tall. Deal with it. */
  overflow-y: auto;
  overflow-x: hidden;
}
</style>
