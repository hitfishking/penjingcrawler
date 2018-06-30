test_mathfunc.py就是一个简单的测试，有几点需要说明的：
1. 在第一行给出了每一个用例执行的结果的标识，成功是 .，失败是 F，出错是 E，跳过是 S。从上面也可以看出，测试的执行跟方法的顺序没有关系，test_divide写在了第4个，但是却是第2个执行的。
2. 每个测试方法均以 test 开头，否则是不被unittest识别的。
3. 在unittest.main()中加 verbosity 参数可以控制输出的错误报告的详细程度，默认是 1，如果设为 0，则不输出每一用例的执行结果，即没有上面的结果中的第1行；如果设为 2，则输出详细的执行结果。

----------------------------------------
测试属于offline task processing类型的应用；
有一个controller，多个worker，包括：TestSuite，runner，都属于worker；main()是controller；
