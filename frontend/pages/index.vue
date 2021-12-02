<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="12" md="12">
      <v-stepper v-model="e1">
        <v-stepper-header>
          <v-stepper-step :complete="e1 > 1" step="1">
            Upload your data
          </v-stepper-step>

          <v-divider></v-divider>

          <v-stepper-step :complete="e1 > 2" step="2">
            Explain your analysis
          </v-stepper-step>

          <v-divider></v-divider>

          <v-stepper-step :complete="e1 > 3" step="3">
            Refine your question
          </v-stepper-step>

          <v-divider></v-divider>

          <v-stepper-step :complete="e1 > 4" step="4">
            Refine your question
          </v-stepper-step>

          <v-divider></v-divider>

          <v-stepper-step :complete="e1 > 5" step="5">
            View your results
          </v-stepper-step>

          <v-divider></v-divider>

          <v-stepper-step :complete="e1 > 6" step="6">
            Tune your pipeline
          </v-stepper-step>
        </v-stepper-header>

        <v-stepper-items>
          <v-stepper-content step="1" class="px-10 pb-8">
            <input-form @sendData="sendFormOnSocket"></input-form>
          </v-stepper-content>

          <v-stepper-content step="2" class="px-10 pb-8">
            <insert-sentence></insert-sentence>
          </v-stepper-content>

          <v-stepper-content step="3" class="px-10 pb-8">
            <tuning-chat :destination="'comprehension'" />
          </v-stepper-content>

          <v-stepper-content step="4" class="px-10 pb-8">
            <tuning-chat :destination="'refinement'" />
          </v-stepper-content>

          <v-stepper-content step="5" class="px-10 pb-8">
            <results></results>

            <v-btn color="secondary" @click="restart()"> Restart </v-btn>
            <v-btn
              v-if="resultsReady"
              color="secondary"
              @click="toFramework({ intent: 'skip' })"
            >
              Continue without choosing a problem
            </v-btn>
          </v-stepper-content>

          <v-stepper-content step="6" class="px-10 pb-8">
            <tuning></tuning>

            <v-btn color="secondary" @click="restart()"> Restart </v-btn>
            <v-btn
              v-if="resultsReady"
              :color="pipelineEdited ? 'primary' : 'secondary'"
              @click="toFramework({ intent: 'run' })"
            >
              Run again
            </v-btn>
          </v-stepper-content>
        </v-stepper-items>
      </v-stepper>
    </v-col>
  </v-row>
</template>

<script src="/socket.io/socket.io.js"></script>
<script>
import io from 'socket.io-client'
import { mapState, mapMutations, mapActions } from 'vuex'
import TuningChat from '../components/TuningChat.vue'

const socket = io('http://127.0.0.1:5000/')

export default {
  components: { TuningChat },
  data() {
    return {
      polling: null,
    }
  },
  computed: {
    ...mapState(['e1', 'resultsReady', 'pipelineEdited']),
  },
  mounted() {
    //this.polling = setInterval(() => this.waitForResults(), 3000)
  },
  methods: {
    ...mapMutations(['setStep', 'setResultsReady', 'setAvailable']),
    ...mapActions(['toFramework', 'waitForResults', 'setComputationResults']),
    restart() {
      this.setAvailable(true)
      this.setResultsReady(false)
      this.setStep(1)
    },
    sendOnSocket(eventType, payolad) {
      console.log('SOCKET', typeof payolad)
      socket.emit(eventType, payolad)
    },
    sendFormOnSocket(payload) {
      this.sendOnSocket('ack', payload)
    },
  },
  created() {
    console.log('created invocato')
    console.log('UELLA', socket.connected)
    console.log('UELLA2')
    socket.on('results', (results) => {
      context.commit('setComputationResults', results)
    })
    //this.sendOnSocket('ack', { message_id: 1, location: 'crated' })
    /*
    socket.on('message_response', (payload) => {
      if (payload.type) {
        console.log('server sent JSON_response', payload)
        this.receiveChat(payload.message)
      } else {
        console.log('ERRORE STRANO', payload)
      }
    })
    socket.on('freeze_chat', () => {
      this.isChatActive = false
    })
    socket.on('unfreeze_chat', () => {
      this.isChatActive = true
    })
    */
  },
}
</script>
