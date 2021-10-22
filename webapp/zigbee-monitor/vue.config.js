module.exports = {
    publicPath: './',
    devServer:{
        //proxy: 'http://localhost:8000'
        proxy:{
            '^/':{
                target: 'http://localhost:8000',
                ws: true,
            }
        }
    },
}