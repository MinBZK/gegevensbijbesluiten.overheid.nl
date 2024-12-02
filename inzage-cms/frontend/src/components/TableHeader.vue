<template>
  <th style="white-space: nowrap">
    {{ header }}
    <!-- <v-icon class="th-icon" :class="{ 'th-icon-filter': !!selectedFilters }" @click="dialog = true">
      mdi-filter
    </v-icon> -->
  </th>
  <v-dialog v-model="dialog" scrollable max-width="600">
    <v-card>
      <v-toolbar color="primary">
        <v-toolbar-title> {{ header }}</v-toolbar-title>
      </v-toolbar>

      <v-card-text>
        <v-checkbox
          v-for="v in values"
          :key="v"
          v-model="checkedValues"
          hide-details
          :label="labelKey && v ? v[labelKey] : v"
          :multiple="true"
          :value="v"
          density="compact"
          :inline="true"
          ma="2"
        />
      </v-card-text>
      <v-divider />
      <v-card-actions>
        <v-btn v-if="checkedValues.length != 0" color="primary" @click="checkedValues = []">
          Filters verwijderen
        </v-btn>
        <v-spacer />
        <v-btn color="primary" @click="dialog = false"> Sluiten </v-btn>
        <v-btn color="primary" @click=";[$emit('setFilter', checkedValues), (dialog = false)]">
          Toepassen
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import type { PropType } from 'vue'

export default defineComponent({
  name: 'TableHeader',
  props: {
    header: {
      type: String,
      default: null,
      required: false
    },
    values: {
      type: Array as PropType<Array<string>>,
      required: true
    },
    selectedFilters: {
      type: Object,
      default: () => {},
      required: false
    },
    labelKey: {
      type: String,
      default: null,
      required: false
    }
  },
  emits: ['setFilter'],
  data() {
    return {
      dialog: false,
      checkedValues: []
    }
  },
  watch: {
    dialog: {
      handler() {
        this.checkedValues = this.selectedFilters ? this.selectedFilters.values : []
      },
      immediate: true,
      flush: 'post'
    }
  }
})
</script>

<style lang="scss" scoped>
@import '/src/styles/styles.scss';

.th-icon {
  color: $tertiary;
  cursor: pointer;
}

.th-icon:hover {
  color: $primary;
}

.th-icon-filter {
  color: $error;
}
</style>
