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
              <v-scale-transition>
                <v-card
                  :color="item.isBot ? 'white' : 'accent'"
                  class="py-1 px-2"
                >
                  {{ item.message }}
                </v-card>
              </v-scale-transition>
              <v-card
                v-if="item.isOption"
                :color="item.isBot ? 'white' : 'accent'"
                class="py-1 px-2"
              >
                <v-btn @click="sendBtn(item.first)">{{ item.first }}</v-btn>
                <v-btn @click="sendBtn(item.second)">{{ item.second }}</v-btn>
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
            :deactivated="isChatActive"
            @click="sendText"
          >
            <font-awesome-icon icon="chevron-right" size="2x" color="white" />
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<!-- <script src="/socket.io/socket.io.js"></script> -->
<script>
import { mapActions, mapState, mapMutations } from 'vuex'
import io from 'socket.io-client'

// const SOCKET_PATH = '/inspire/socket.io'
// const SOCKET_ENDPOINT = '/test'
const socket = io('http://127.0.0.1:5000/')

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
      isChatActive: true,
      lastMessage: '',
    }
  },
  computed: {
    ...mapState([
      'tuningChat',
      'comprehensionChatCompleted',
      'sessionId',
      'comprehensionPipeline',
      'comprehensionConversationState',
    ]),
  },
  updated() {
    this.scrollToEnd()
  },
  created() {
    if (
      // this.destination === 'refinement' ||
      this.destination === 'comprehension'
    ) {
      console.log('UELLA', socket.connected)
      socket.emit('ack', { message_id: 1, location: 'crated' })
      console.log('UELLA2')
      socket.on('message_response', (payload) => {
        console.log('comparo stringhe', this.lastMessage, payload.message)
        if (this.lastMessage !== payload.message) {
          if (payload.type) {
            console.log('server sent JSON_response', payload)
            this.receiveChat(payload.message)
          } else {
            console.log('ERRORE STRANO', payload)
          }
        }
      })
      socket.on('message_binary_option', (payload) => {
        this.receiveChatOption(payload)
      })
      socket.on('comprehension_response', (payload) => {
        console.log('server sent JSON_response', payload)
        if (this.lastMessage !== payload.message) {
          this.lastMessage = payload.message
          this.receiveChat(payload.message)
          this.setComprehensionConversationState(payload.comprehension_state)
          if (payload.show != null) {
            console.log('payload non è null!')
            this.setImageToShow(payload.show)
          }
          if (payload.complete) {
            this.setStep(4)
            socket.emit('execute', {
              comprehension_pipeline: this.comprehensionPipeline,
            })
          }
        }
        socket.on('results', (response) => {
          console.log('ho ricevuto questo', response)
          this.setRequestDescription(response.request)
          this.setStep(5)
          this.receiveChat(response.comprehension_sentence)
          this.setImage(response.img)
        })

        /*
        if (payload.type) {
          console.log('server sent JSON_response', payload)
          this.receiveChat(payload.message)
        } else {
          console.log('ERRORE STRANO', payload)
        } */
      })
      socket.on('freeze_chat', () => {
        this.isChatActive = false
      })
      socket.on('unfreeze_chat', () => {
        this.isChatActive = true
      })
      /*
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
      }) */
    }
  },
  methods: {
    sendBtn(inputData) {
      this.utterance = inputData
      this.sendSocketMessage('message_sent')
      console.log(inputData)
    },
    ...mapActions(['toFramework', 'sendChatMessage']),
    ...mapMutations([
      'sendChat',
      'receiveChat',
      'receiveChatOption',
      'setComprehensionChatCompleted',
      'setComprehensionConversationState',
      'setStep',
      'setRequestDescription',
      'setImage',
      'setImageToShow',
    ]),
    sendText() {
      if (this.isChatActive) {
        if (this.utterance.trim() !== '' && this.utterance !== '\n') {
          if (this.destination === 'mmcc') this.toFramework(this.utterance)
          else if (this.destination === 'comprehension') {
            this.sendSocketMessage('comprehension')
            // const res = this.sendChatMessage({
            //  destination: this.destination,
            //  message: this.utterance,
            // })
            // .then(function (response) {
            //  console.log('RES:', response.completed)
            // })
          } else if (this.destination === 'refinement') {
            this.sendSocketMessage('message_sent')
          }
          this.utterance = ''
        }
      }
    },
    scrollToEnd() {
      const container = this.$el.querySelector('#chat')
      // console.log(container);
      if (container) {
        container.scrollTop = container.scrollHeight
      }
    },
    sendSocketMessage(destination) {
      this.sendChat(this.utterance)
      if (destination === 'comprehension') {
        const payload = {}
        payload.message = this.utterance
        payload.comprehension_state = this.comprehensionConversationState
        payload.session_id = this.sessionId
        payload.comprehension_pipeline = this.comprehensionPipeline
        console.log('mandato a comprehension')
        socket.emit(destination, payload)
      } else {
        socket.emit(destination, { message: this.utterance })
      }
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
