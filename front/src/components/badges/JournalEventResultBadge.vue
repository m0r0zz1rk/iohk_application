<template>
  <ui5-badge v-if="result === 'NONE'" color-scheme="10">Без результата</ui5-badge>
  <ui5-badge v-if="result === 'SUCCESS'" color-scheme="7">Успешно</ui5-badge>
  <ui5-badge v-if="result === 'INFO'" color-scheme="1">Информация</ui5-badge>
  <ui5-badge v-if="result === 'ERROR'" color-scheme="3">Ошибка</ui5-badge>
</template>

<script>
export default {
  name: 'JournalEventResultBadge',
  props: {
    result: {type: String}
  }
}

</script>

<style scoped>

</style>