defmodule Sol do
  @type levelorder :: nil | :positive | :negative

  def main do
    input = parseInput()
    proc(input)
  end

  def example do
    input = [
      [1,3,5,7],
      [7,6,3,1],
      [7,5,5,1],
      [1,5,7,9]
    ]
    proc(input)
  end

  def proc([report | rest]) do
    is_safe(report, nil) + proc(rest)
  end
  def proc([]) do 0 end

  def is_safe([curr | tail = [next | rest]], nil) do
    diff = curr - next
    a = abs(diff)

    if a <= 0 || a > 3 do
      0
    else
      if diff < 0 do
        is_safe(tail, :positive)
      else
        is_safe(tail, :negative)
      end
    end
  end

  def is_safe([curr | tail = [next | rest]], :positive) do
    diff = curr - next
    a = abs(diff)

    if a <= 0 || a > 3 do
      0
    else
      if diff > 0 do
        0
      else
        is_safe(tail, :positive)
      end
    end
  end

  def is_safe([curr | tail = [next | rest]], :negative) do
    diff = curr - next
    a = abs(diff)

    if a <= 0 || a > 3 do
      0
    else
      if diff < 0 do
        0
      else
        is_safe(tail, :negative)
      end
    end
  end

  def is_safe([curr | []], _) do 1 end
  def is_safe([],_) do 1 end

  def parseInput do
    fPath = "input.txt"
    {:ok, data} = File.read(fPath)
    data = String.split(data, "\n", trim: true)

    reports =
      Enum.map(data, fn v ->
        sp = String.split(v, ~r{\s+})
        Enum.map(sp, fn e -> String.to_integer(e) end)
      end)

    File.write("output.txt",reports);
    reports
  end
end
