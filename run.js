function RUN()
{
    var python = requirejs('child_process').spawn('python', ['./hello.py']);

    	var x = document.getElementById("MIPS").value;
    	console.log(x);
//         import { run } from 'python-shell';

//     run('hello.py',  function  (err, results)  {
//     if  (err)  throw err;
//     console.log('hello.py finished.');
//     console.log('results', results);
//   });
}