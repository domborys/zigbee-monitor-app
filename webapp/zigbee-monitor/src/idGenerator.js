export default function idGenerator(){
    let id = 1;
    function next(){
        return id++;
    }
    return {next:next};
}