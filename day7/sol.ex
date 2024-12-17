
defmodule Sol do


  def part1 do
    equations = parseInput()
    proc1(equations,0)
  end

  def part2 do
    equations = parseInput()
    proc2(equations, 0)
  end

  def example do
    input="190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"
    equations=parse(input)
    IO.inspect(equations)
    {proc1(equations, 0), proc2(equations,0)}

  end

  def proc2([], sum) do sum end
  def proc2(equations=[{value, operands=[first|restops]}|rest], sum) do
    proc2(rest, sum + validateVal2(restops, value, first))
  end


  def proc1([], sum) do sum end
  def proc1(equations=[{value, operands=[first|restops]}|rest], sum) do
    proc1(rest, sum + validateVal(restops, value, first))
  end

  def validateVal([], seekedVal, accVal) when seekedVal === accVal do accVal end
  def validateVal([], seekedVal, accVal) do 0 end
  def validateVal(operands=[curr|rest], seekedVal, accVal) do
    lval=validateVal(rest, seekedVal, accVal + curr)
    if(lval !== 0) do lval else validateVal(rest, seekedVal, accVal * curr)  end
  end


  def validateVal2([], seekedVal, accVal) when seekedVal === accVal do accVal end
  def validateVal2([], seekedVal, accVal) do 0 end
  def validateVal2(operands=[curr|rest], seekedVal, accVal) do
    lval=validateVal2(rest, seekedVal, accVal + curr)
    if(lval !== 0) do lval
    else
      rval=validateVal2(rest, seekedVal, accVal * curr)
      if (rval !== 0) do rval
      else validateVal2(rest, seekedVal, String.to_integer(to_string(accVal)<>to_string(curr)))
      end
    end
  end


  def parseInput do
    filePath="input.txt"
    {:ok, data} = File.read(filePath)
    parse(data)
  end

  def parse(data) do
    equations = String.split(data, "\n")
    equations = Enum.map(equations, fn eq->
      [value, operands] = String.split(eq, ":")
      operands = String.split(operands)|>Enum.map(fn e-> String.to_integer(e) end)
      {String.to_integer(value), operands}
    end)
  end
end
