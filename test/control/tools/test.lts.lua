    for i=1,1 do
        if (getInput(0)==0) then
            setSpeed(40)
            on(30)
            emgStop(0)
            luaSleep(2.000000)
            setAccel(10)
        end --#END -- 2
        while (getInput(3)==0 and targetOK(P2)==0) do
        end --#END -- 3
    end --#END -- 1
