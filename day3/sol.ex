
defmodule Sol do

  def main do
    input = parseInput()
    matches = Regex.scan(~r/mul\([0-9]{1,3},[0-9]{1,3}\)/, input)
    proc(matches)
  end

  def proc([[curr|_]|tail]) do
    [[a],[b]] = Regex.scan(~r/[0-9]+/, curr)
    a = String.to_integer(a)
    b = String.to_integer(b)
    (a*b) + proc(tail)
  end
  def proc([]) do 0 end


  def parseInput do
    fPath = "input.txt"
    {:ok, data} = File.read(fPath)
    data
  end
end
