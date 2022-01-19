<template>
  <div>
    <v-card
      class="mb-12"
      :height="jsonDataset == null ? '240px' : '850px'"
      flat
    >
      <v-file-input
        v-model="dataset"
        truncate-length="15"
        :error="fileInputError"
        label="select a CSV"
        @change="showSecondPart = false"
      ></v-file-input>
      <v-switch
        v-model="hasIndex"
        flat
        :label="`The file rows have ${hasIndex ? '' : 'not'} indices`"
        @change="showSecondPart = false"
      ></v-switch>
      <v-switch
        v-model="hasColumnNames"
        flat
        :label="`The file rows have ${
          hasColumnNames ? '' : 'not'
        } column names`"
      ></v-switch>
      <!--
      <v-flex xs5>
        <v-select
          v-model="separator"
          :items="separator_list"
          :item-text="'text'"
          :item-value="'value'"
          :error="separatorError"
          label="Separator"
        ></v-select>
      </v-flex>
      -->
      <v-btn
        v-if="!showSecondPart"
        color="primary"
        :disabled="dataset == null"
        @click="parse"
      >
        Upload Dataset
      </v-btn>

      <v-card v-if="showSecondPart" flat>
        {{ previewSentence }}
        <v-alert v-if="!hasColumnNames" type="warning" color="grey"
          >The first line of the CSV has been omitted in the preview, but it
          will be used in the analysis as well</v-alert
        >
        <v-data-table
          height="500px"
          dense
          :items="jsonDataset"
          :headers="columnNamesDictionary"
          :item-key="columnNamesDictionary[0]"
        ></v-data-table>
        <v-flex xs7>
          <v-flex xs5>
            <v-autocomplete
              v-model="label"
              :items="labelsDictionary"
              :item-text="'text'"
              :item-value="'value'"
              :error="separatorError"
              label="Label"
            ></v-autocomplete>
          </v-flex>
        </v-flex>
        <v-btn color="primary" @click="sendData"> Continue </v-btn>
      </v-card>
    </v-card>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import Papa from 'papaparse'

export default {
  components: {},
  data() {
    return {
      hasIndex: true,
      hasColumnNames: true,
      separator_list: [
        { text: ',', value: ',' },
        { text: ';', value: ';' },
        { text: '\\t', value: '\t' },
      ],
      separator: '',
      dataset: null,
      jsonDataset: null,
      fileInputError: false,
      separatorError: false,
      fileInputHint: '',
      label: '',
      columnNamesDictionary: [],
      columnNamesArray: [],
      showSecondPart: false,
      labelsDictionary: [],
      previewSentence:
        'Here is a preview of your data, (limited to 30 elements)',
    }
  },
  computed: {},
  methods: {
    sendData() {
      this.fileInputError = !this.dataset
      this.separatorError = !this.separator
      if (!this.fileInputError && !this.separatorError) {
        this.fileInputError = false
        this.separatorError = false
        const inputData = {
          ds: this.dataset,
          hasColumnNames: this.hasColumnNames,
          hasIndex: this.hasIndex,
          separator: this.separator,
          format: '.csv',
          label: this.label,
        }
        // this.$emit('sendData', inputData)
        this.sendDataStore(inputData)
      }
    },
    parse() {
      if (this.dataset == null) return
      const parsed = Papa.parse(this.dataset, {
        header: true,
        skipEmptyLines: true,
        preview: 30,
        complete: function (results) {
          this.columnNamesDictionary = []
          let i = 0
          const fieldsNames = []
          const cap = Math.min(results.meta.fields.length, 30)

          for (i = 0; i < cap; i++) {
            const name = results.meta.fields[i]
            const objectino = {
              text: this.hasColumnNames ? results.meta.fields[i] : i,
              value: results.meta.fields[i],
            }
            this.columnNamesDictionary.push(objectino)
            fieldsNames.push(name)
          }
          this.columnNamesArray = fieldsNames
          // this.labelsDictionary = [...this.columnNamesDictionary]
          this.labelsDictionary = results.meta.fields
          this.labelsDictionary.unshift({
            text: '(None)',
            value: '',
          })
          this.jsonDataset = results.data
          this.separator = results.meta.delimiter
          if (results.meta.fields.length > 30) {
            this.previewSentence +=
              '. We show only the first 30 columns, but all the data will be used in the analysis'
          } else {
            this.previewSentence +=
              'Here is a preview of your data, (limited to 30 elements)'
          }
          this.showSecondPart = true
        }.bind(this),
      })
      return parsed
    },
    ...mapActions(['setStep', 'sendDataStore']),
  },
}
</script>
