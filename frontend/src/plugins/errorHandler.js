export default {
    install(Vue) {
    Vue.prototype.$errorHandler = function(err , Text=undefined) {
        console.log('errHandlr', err)
        let errStatus
        let errText = ''
        if(!err){
            errStatus = ''
            errText = Text
        }else{
            errStatus = err.response.status
            if (err.response) {
                if (Array.isArray(err.response.data)){
                    errText = err.response.data[0]
                }else if(typeof err.response.data === 'object'){
                    let obj = err.response.data
                    errText = Object.keys(obj)[0] +" : "+ Object.values(obj)[0]
                }else if(!!err.response.data.error){
                    errText = err.response.data.error
                }else{
                    errText = err.response.statusText
                }
            }
            else if (err.request) {
                errText = err.request.statusText
            }
            if (!!Text){
                errText += '<br>'+Text 
            }
        }

        this.$notify({
        message:
        `에러 <b>${errStatus}</b> - ${errText}`,
        timeout: 30000,
        icon: 'tim-icons icon-bell-55',
        horizontalAlign: 'right',
        verticalAlign: 'top',
        type: 'warning'
    });
    }

    
    }
};
  