Test task 2
In this task, you will create two programs that interact with each other through standard input and output.

Program A: Pseudo-Random Number Generator
Program A will act as a pseudo-random number generator. It reads commands from stdin, where each command is delimited by a line break, and writes responses to stdout. The program should handle the following commands:

Hi: Responds with "Hi" on stdout.
GetRandom: Responds with a pseudo-random integer on stdout.
Shutdown: Gracefully terminates the program.
Any unknown commands should be ignored.

Program B: Controller
Program B will launch Program A as a separate process, provided as an argument. Once Program A is running, Program B should:

Send the Hi command to Program A and verify the correct response.
Retrieve 100 random numbers by sending the GetRandom command to Program A 100 times.
Send the Shutdown command to Program A to terminate it gracefully.
Sort the list of retrieved random numbers and print the sorted list to the console.
Calculate and print the median and average of the numbers.
Additional Information
Languages: You may use Kotlin or Python for this task. Each program can be written in either language, and using the same language for both programs is acceptable.

Process Requirements: Programs A and B must be launched in separate processes and communicate exclusively through stdin and stdout.

Bonus Points: Awarded for robustness and code quality, including code style, documentation, and structure.

Submission: Share your completed programs via a GitHub repository or a similar platform. Please include instructions on how to compile (if necessary), run, and test the programs.