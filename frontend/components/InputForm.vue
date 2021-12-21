<template>
  <div>
    <v-card class="mb-12" height="300px" flat>
      <v-file-input
        v-model="dataset"
        truncate-length="15"
        :error="fileInputError"
        label="select a CSV"
        @change="parse"
      ></v-file-input>
      <!-- <v-layout row wrap justify-center> -->
      <!-- <v-flex xs5> -->
      <v-switch
        v-model="hasIndex"
        flat
        :label="`The file rows have ${hasIndex ? '' : 'not'} indices`"
      ></v-switch>
      <!-- </v-flex> -->
      <!-- <v-flex xs6> -->
      <v-switch
        v-model="hasColumnNames"
        flat
        :label="`The file rows have ${
          hasColumnNames ? '' : 'not'
        } column names`"
      ></v-switch>
      <!-- </v-flex> -->
      <!-- </v-layout> -->
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
      <v-data-table
        v-if="jsonDataset != null"
        :items="jsonDataset"
        :headers="columnNames"
        :item-key="columnNames[0]"
      ></v-data-table>
      <v-flex xs7>
        <v-text-field
          v-model="label"
          label="Label (leave blank if not present)"
        ></v-text-field>
      </v-flex>
    </v-card>
    <!-- <v-btn color="primary"> Continue </v-btn> -->
    <v-btn color="primary" @click="sendData"> Continue </v-btn>
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
      columnNames: [],
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
      const parsed = Papa.parse(this.dataset, {
        header: this.hasColumnNames,
        skipEmptyLines: true,
        complete: function (results) {
          for (const name in results.meta.fields) {
            const objectino = {
              text: results.meta.fields[name],
              value: results.meta.fields[name],
            }
            console.log('objectino', objectino)
            this.columnNames.push(objectino)
          }
          // nthis.columnNames = results.meta.fields
          this.jsonDataset = results.data
          // this.parsed = true;
          console.log('Parsed', results)
          console.log('column names', this.columnNames)
        }.bind(this),
      })
      return parsed
    },
    ...mapActions(['setStep', 'sendDataStore']),
  },
}
</script>
