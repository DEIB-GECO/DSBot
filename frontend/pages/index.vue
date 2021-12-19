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
            <input-form></input-form>
          </v-stepper-content>

          <v-stepper-content step="2" class="px-10 pb-8">
            <insert-sentence></insert-sentence>
          </v-stepper-content>

          <v-stepper-content step="3" class="px-10 pb-8">
            <v-row align="center" justify="center">
              <v-col>
                <tuning-chat :destination="'comprehension'" />
              </v-col>
              <v-col v-show="imageToShow != ''" cols="7" sm="7" md="7">
                <v-expand-x-transition>
                  <v-card flat>
                    Here is an example to better explain it!
                    <v-divider></v-divider>
                    <img
                      v-if="imageToShow == 'classification'"
                      src="~/assets/classification.jpg"
                      style="max-width: 100%"
                    />
                    <img
                      v-if="imageToShow == 'correlation'"
                      src="~/assets/correlation.jpg"
                      style="max-width: 100%"
                    />
                    <img
                      v-if="imageToShow == 'association_rules'"
                      src="~/assets/association_rules.jpg"
                      style="max-width: 100%"
                    />
                    <img
                      v-if="imageToShow == 'regression'"
                      src="~/assets/regression.jpg"
                      style="max-width: 100%"
                    />
                    <v-btn @click="setImageToShow('')" color="primary"
                      >GOTCHA</v-btn
                    >
                  </v-card>
                </v-expand-x-transition>
              </v-col>
            </v-row>
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

<!-- <script src="/socket.io/socket.io.js"></script> -->
<script>
// import io from 'socket.io-client'
import { mapState, mapMutations, mapActions, mapGetters } from 'vuex'
import TuningChat from '../components/TuningChat.vue'

// const socket = io('http://127.0.0.1:5000/')

export default {
  components: { TuningChat },
  data() {
    return {
      polling: null,
      isVisible: true,
    }
  },
  computed: {
    ...mapGetters(['getComprehensionChatCompleted']),
    ...mapState([
      'e1',
      'resultsReady',
      'pipelineEdited',
      'comprehensionChatCompleted',
      'imageToShow',
    ]),
  },
  whatch: {
    e1(old, newV) {
      console.log('AASASSAASAS')
    },
  },
  mounted() {
    // this.polling = setInterval(() => this.waitForResults(), 3000)
  },
  methods: {
    ...mapMutations([
      'setStep',
      'setResultsReady',
      'setAvailable',
      'setRequestDescription',
      'receiveChat',
      'receiveChatOption',
      'setImage',
      'setImageToShow',
    ]),
    ...mapActions(['toFramework', 'waitForResults', 'setComputationResults']),
    restart() {
      this.setAvailable(true)
      this.setResultsReady(false)
      this.setStep(1)
    },
    sendOnSocket(eventType, payolad) {
      console.log('SOCKET', typeof payolad)
      // socket.emit(eventType, payolad)
    },
    emitComputationResults(results) {
      // context.commit('setComputationResults', results)
    },
    launchExecution() {
      console.log('AAAAAA')
    },
  },
}
</script>
