
const { createApp } = Vue
//import { createApp } from 'vue'
const API_URL =  'https://www.flickr.com/services/rest/?method=flickr.galleries.getPhotos&api_key=56ae4807801f209030ecf81960cb5fc0&gallery_id=72157720775891722&format=json&nojsoncallback=1'

const API_KEY = '56ae4807801f209030ecf81960cb5fc0'

createApp({
    data: () => ({
        gallery: null,
        photos: [],
        message: 'Hewwo'
    }),

    created() {
        this.fetchData()
    },

    methods: {
        async fetchData() {
            const url = `${API_URL}`
            this.gallery = await (await fetch(url)).json()
            this.gallery = this.gallery.photos.photo
            console.log(this.gallery)
            for(index in this.gallery) {
                let item = this.gallery[index] 
                this.photos.push(`https://live.staticflickr.com/${item.server}/${item.id}_${item.secret}_w.jpg`)
            }
        }
    }
}).mount('#app')
