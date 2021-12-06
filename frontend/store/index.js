export const state = () => ({
  e1: 1,
  sessionId: 1,
  requestDescription: '',
  resultsReady: true,
  imageBase64: null,
  resultsDetails: '',
  tuningChat: [],
  tuningPipeline: [],
  backendAvailable: true,
  pipelineEdited: false,
  comprehensionConversationState: '',
  comprehensionPipeline: '',
  comprehensionChatCompleted: false,
})

export const getters = {
  getComprehensionChatCompleted: (state) => {
    return state.comprehensionChatCompleted
  },
}

export const mutations = {
  setStep(state, newValue) {
    state.e1 = newValue
  },
  setSessionId(state, newId) {
    state.sessionId = newId
  },
  setRequestDescription(state, newRequest) {
    state.requestDescription = newRequest
  },
  setResultsReady(state, newState) {
    state.resultsReady = newState
  },
  setImage(state, image) {
    state.imageBase64 = image
  },
  setResultsDetails(state, details) {
    state.resultsDetails = details
  },
  sendChat(state, msg) {
    state.tuningChat.push({ isBot: false, message: msg })
  },
  receiveChat(state, msg) {
    if (msg) state.tuningChat.push({ isBot: true, message: msg })
  },
  setTuningPipeline(state, pipeline) {
    state.tuningPipeline = pipeline
  },
  setAvailable(state, available) {
    state.backendAvailable = available
  },

  setPipelineEdited(state, edited) {
    state.pipelineEdited = edited
  },

  setComprehensionConversationState(state, newState) {
    state.comprehensionConversationState = newState
    console.log('new comprehension state', newState)
  },

  setComprehensionPipeline(state, newPipeline) {
    state.comprehensionPipeline = newPipeline
  },

  setComprehensionChatCompleted(state, newValue) {
    console.log(
      'Ho messo comprehension da a',
      state.comprehensionChatCompleted,
      this.newValue
    )
    state.comprehensionChatCompleted = true
    console.log('Ora vale', state.comprehensionChatCompleted)
  },
}

export const actions = {
  async sendDataStore(context, inputData) {
    console.log('AAA', inputData)
    const formdata = new FormData()
    formdata.append('has_column_names', inputData.hasColumnNames)
    formdata.append('ds', inputData.ds)
    formdata.append('has_index', inputData.hasIndex)
    formdata.append('separator', inputData.separator)
    formdata.append('format', inputData.format)
    formdata.append('label', inputData.label)

    console.log('FormData')
    for (const value of formdata.values()) {
      console.log(value)
    }

    const res = await this.$axios
      .post('/receiveds', formdata, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      .then(function (response) {
        context.commit('setSessionId', response.data.session_id)
        context.commit('setStep', 2)
      })
      .catch(function (e) {
        console.log('FAILURE!!', e)
      })
    return res
  },

  async sendUtterance(context, sentence) {
    if (sentence === '') return null

    context.commit('receiveChat', 'What do you want to obtain?')
    context.commit('sendChat', sentence)

    const bodyRequest = {
      session_id: this.state.sessionId,
      message: sentence,
    }
    console.log('Ho ricevuto questo', bodyRequest)
    const res = await this.$axios
      .post('/utterance', bodyRequest)
      .then(function (response) {
        console.log('REST: ho ricevuto questo', response.data)
        context.commit('setRequestDescription', response.data.request)
        context.commit('setStep', 3)
        context.commit('receiveChat', response.data.comprehension_sentence)
        context.commit(
          'setComprehensionConversationState',
          response.data.comprehension_state
        )
        context.commit(
          'setComprehensionPipeline',
          response.data.comprehension_pipeline
        )
      })
    console.log(
      'Ora comprehension vale: ',
      this.state.comprehensionConversationState
    )
    return res
  },

  setComputationResults(context, response) {
    console.log('ho ricevuto questo', response)
    context.commit('setRequestDescription', response.request)
    context.commit('setStep', 4)
    context.commit('receiveChat', response.comprehension_sentence)
    context.commit('setImage', response.img)
    console.log('Ora img vale', context.state.imageBase64)
  },

  async waitForResults(context) {
    console.log('WAIT FOR RESULTS', this.state.e1)
    if (this.state.e1 === 4 && !this.state.resultsReady) {
      console.log('GET RESULTS CALLED')
      const pollingResponse = await this.$axios
        .get(`/results/${this.state.sessionId}`)
        .then(function (response) {
          console.log(response)
          if (response.data.ready) {
            context.commit('setImage', response.data.img)
            context.commit('setResultsDetails', response.data.details)
            context.commit('setResultsReady', response.data.ready)
            context.commit('receiveChat', response.data.tuning.utterance)
            context.commit('setPipelineEdited', false)
          } else {
            console.log('Non faccio niente')
          }
        })
      return pollingResponse
    }

    return null
  },

  async toFramework(context, data) {
    if (!this.state.backendAvailable) {
      return null
    }
    context.commit('setAvailable', false)

    const isUtterance = typeof data === 'string' || data instanceof String
    let bodyRequest
    if (isUtterance) {
      context.commit('sendChat', data)
      bodyRequest = {
        session_id: this.state.sessionId,
        type: 'utterance',
        utterance: data,
      }
    } else {
      bodyRequest = {
        session_id: this.state.sessionId,
        type: 'payload',
        payload: data,
      }
    }
    const res = await this.$axios
      .post('/tuning', bodyRequest)
      .then(function (response) {
        console.log(response)

        if ('utterance' in response.data.tuning) {
          context.commit('receiveChat', response.data.tuning.utterance)
        }
        if ('payload' in response.data.tuning) {
          if (response.data.tuning.payload.status === 'choose_problem') {
            // context.commit('setStep', 3) // Assume already in step 3 and can't come back from 4
            context.commit('setImage', response.data.tuning.payload.result)
          } else if (response.data.tuning.payload.status === 'edit_param') {
            console.log('unooo')
            context.commit('setStep', 5)
            context.commit(
              'setTuningPipeline',
              response.data.tuning.payload.pipeline
            )
          } else if (response.data.tuning.payload.status === 'end') {
            context.commit('setResultsReady', false)
            context.commit('setStep', 3)
          } else {
            console.log(
              'Unknown tuning status:',
              response.data.tuning.payload.status
            )
          }
        }

        context.commit('setAvailable', true)
      })
    return res
  },

  async sendChatMessage(context, data) {
    // The data can be {destination: '/yourDestination', message: userUtterance}

    // Add the message to the chat panel
    context.commit('sendChat', data.message)

    let res = null

    // This is the data sent to the backend
    if (data.destination === 'comprehension') {
      console.log('Eseguito comprehension')
      const bodyRequest = {
        message: data.message,
        comprehension_state: this.state.comprehensionConversationState,
        session_id: this.state.sessionId,
        comprehension_pipeline: this.state.comprehensionPipeline,
      }
      res = await this.$axios
        .post(data.destination, bodyRequest)
        .then(function (response) {
          console.log('response:', response.data)
          // Add the response to the chat panel
          context.commit('receiveChat', response.data.message)
          context.commit(
            'setComprehensionConversationState',
            response.data.comprehension_state
          )
          if (response.data.complete) {
            console.log('dueeee')

            context.commit('setStep', 5)
            context.commit('setComprehensionChatCompleted', true)
          }
          // Do something with the response if necessary, for example:
          // console.log(response)
        })
    } else {
      console.log('eseguito else')
      const bodyRequest = {
        message: data.message,
      }
      res = await this.$axios
        .post(data.destination, bodyRequest)
        .then(function (response) {
          console.log('response:', response.data)
          // Add the response to the chat panel
          context.commit('receiveChat', response.data.message)
          // Do something with the response if necessary, for example:
          // console.log(response)
        })
    }
    return res
  },
}
