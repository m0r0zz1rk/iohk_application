<template>
  <Editor class="tiny-mce"
      v-model="editorText"
      :api-key="TinyMCEAPIKey"
      :init="{
         height: editorHeight,
         menubar: 'edit table',
         language: 'ru',
         plugins: [
           'advlist autolink lists link image charmap print preview anchor',
           'searchreplace visualblocks code fullscreen',
           'insertdatetime media table paste code help wordcount'
         ],
         content_style: `
            body {
              background: #fff;
              font-size: 36pt;
            }
         `,
         toolbar:
           'undo redo | bold italic underline strikethrough | \
           fontselect fontsizeselect formatselect | \
           alignleft aligncenter alignright alignjustify | \
           outdent indent |  numlist bullist checklist | \
           forecolor backcolor casechange permanentpen formatpainter removeformat | \
           pagebreak | charmap emoticons | preview save | \
           insertfile image pageembed template link codesample | \
           a11ycheck ltr rtl',
         images_upload_handler: (blobInfo, success, failure) => {
           imagesUploadHandler(blobInfo, success, failure)
         }
      }"
  />
</template>

<script>
import Editor from '@tinymce/tinymce-vue'
import {apiRequest} from "../additional/functions/api_request.js";

export default {
  name: 'TinyMCE',
  components: {Editor},
  props: {
    Information: {type: String},
    additionalData: {type: Object},
    editorHeight: {type: Number}
  },
  data() {
    return {
      editorText: '',
      TinyMCEAPIKey: import.meta.env.VITE_APP_TINYMCE_API_KEY
    }
  },
  methods: {
    init() {
      this.editorText = this.Information
    },
    async imagesUploadHandler(blobInfo, success, failure) {
      let formRequest = new FormData()
      formRequest.append('file', blobInfo.blob(), blobInfo.filename())
      if (this.additionalData) {
        formRequest.append('name', this.additionalData['name'])
      } else {
        formRequest.append('name', 'Изображение')
      }

      apiRequest(
          '/api/v1/commons/tinymce_image/',
          'PUT',
          true,
          formRequest,
          true,
          false
      )
          .then(data => {
            if (data.location) {
              success(data.location)
            } else {
              failure(data.error)
            }
          })
    }
  },
  mounted() {
    this.init()
  }
}
</script>

<style scoped>

</style>