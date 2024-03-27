<template>
  <ui5-badge v-if="['DRAFT', 'Черновик'].includes(status)" color-scheme="5">Черновик</ui5-badge>
  <ui5-badge v-if="['CREATED', 'Сохранена'].includes(status)" color-scheme="7">Сохранена</ui5-badge>
  <ui5-badge v-if="['SHIPPED', 'Отправлена'].includes(status)" color-scheme="1">Отправлена</ui5-badge>
  <ui5-badge v-if="['ACCEPTED', 'Принята'].includes(status)" color-scheme="8">Принята</ui5-badge>
  <ui5-badge v-if="['REJECTED', 'Отклонена'].includes(status)" color-scheme="3">Отклонена</ui5-badge>
  <ui5-badge v-if="['REVOKED', 'Отозвана'].includes(status)" color-scheme="10">Отозвана</ui5-badge>
  <ui5-badge v-if="['COMPLETED', 'Завершена'].includes(status)" color-scheme="6">Завершена</ui5-badge>
</template>

<script>
export default {
  name: 'AppStatus',
  props: {
    status: {type: String}
  }
}

</script>

<style scoped>

</style>