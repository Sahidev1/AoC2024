
defmodule Sol do

  def main do
    [i1, i2] = parseInput()
    dSum = proc(Enum.sort(i1), Enum.sort(i2));
  end

  def proc([i1v|t1], [i2v|t2]) do
    proc(t1, t2) + abs(i1v - i2v)
  end
  def proc([],_) do 0 end
  def proc(_,[]) do 0 end

  def parseInput do
    fPath="input.txt"
    {:ok, data} = File.read(fPath)
    data = String.split(data, "\n", trim: true)
    vals = Enum.map(data, fn e-> Enum.map(String.split(e, ~r{\s+}), fn x->
      String.to_integer(x)
      end)
    end)

    vals = Enum.reduce(vals, [[],[]], fn e, acc ->
      [lacc, racc] = acc
      [lval, rval] = e
      lacc = lacc++[lval]
      racc = racc++[rval]
      [lacc, racc]
    end)
    vals

  end
end