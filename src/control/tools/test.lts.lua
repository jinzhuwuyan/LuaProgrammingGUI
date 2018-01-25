    for i=0,1 do
        if (getInput(0)==0) then
            setSpeed(100)
            setAccel(100)
            luaSleep(10.000000)
            go(P1)
            luaSleep(10.000000)
            go(P7)
            luaSleep(10.000000)
            if (getInput(5)==0) then
                move(P5)
                luaSleep(10.000000)
                if (getInput(4)==0) then
                    off(15)
                end --#END -- 4
            end --#END -- 3
        end --#END -- 2
    end --#END -- 1
