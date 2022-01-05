<template>
  <div>
    <v-card
      class="mb-12"
      :height="jsonDataset == null ? '240px' : '840px'"
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
        @click="parse"
        :disabled="dataset == null"
      >
        Upload Dataset
      </v-btn>

      <v-card v-if="showSecondPart" flat>
        Here is a preview of your data, (limited to 30 elements)
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
            <v-select
              v-model="label"
              :items="labelsDictionary"
              :item-text="'text'"
              :item-value="'value'"
              :error="separatorError"
              label="Label"
            ></v-select>
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
          for (const name in results.meta.fields) {
            const objectino = {
              text: this.hasColumnNames ? results.meta.fields[name] : i,
              value: results.meta.fields[name],
            }
            this.columnNamesDictionary.push(objectino)
            i++
          }
          this.columnNamesArray = results.meta.fields
          this.labelsDictionary = [...this.columnNamesDictionary]
          this.labelsDictionary.unshift({
            text: '(None)',
            value: '',
          })
          this.jsonDataset = results.data
          // this.parsed = true;
          this.separator = results.meta.delimiter
          console.log('Delimiter is', results.meta.delimiter)
          this.showSecondPart = true
        }.bind(this),
      })
      return parsed
    },
    ...mapActions(['setStep', 'sendDataStore']),
  },
}
</script>
