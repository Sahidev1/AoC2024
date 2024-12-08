
defmodule Sol do

  def part1 do
    input = parseInput()
    matches = Regex.scan(~r/mul\([0-9]{1,3},[0-9]{1,3}\)/, input)
    proc1(matches)
  end

  def part2 do
    input = parseInput()
    input = "do()"<>input<>"don't()"
    input = String.replace(input, ~r/\s+/, "")

    all = Regex.scan(~r/(?<=do\(\)).+?(?=don't\(\))/, input)|>Enum.map(fn [e|_]->e end)


    sum = Enum.reduce(all, 0, fn str,acc ->
      matches = Regex.scan(~r/mul\([0-9]{1,3},[0-9]{1,3}\)/, str)
      acc + proc1(matches)
    end)
  end

  def example2 do
    input = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    input = input<>"don't()"
    [first_enabled|_] = Regex.run(~r/.+?(?=don't\(\))/m, input)
    rest = Regex.scan(~r/(?<=do\(\)).+?(?=don't\(\))/m, input)
    all = [first_enabled| rest]
    enabledInstructions = Enum.join(all)
    matches = Regex.scan(~r/mul\([0-9]{1,3},[0-9]{1,3}\)/, enabledInstructions)
    proc1(matches)
  end


  def proc1([[curr|_]|tail]) do
    [[a],[b]] = Regex.scan(~r/[0-9]+/, curr)
    a = String.to_integer(a)
    b = String.to_integer(b)
    (a*b) + proc1(tail)
  end
  def proc1([]) do 0 end


  def parseInput do
    fPath = "input.txt"
    {:ok, data} = File.read(fPath)
    data
  end
end
