defmodule Sol do
  @type levelorder :: nil | :positive | :negative

  def part1 do
    input = parseInput()
    proc1(input)
  end

  def part2 do
    input = parseInput()
    cnt = length(input)
    IO.puts("count is: #{cnt}")
    unsafeReps = Enum.filter(input, fn e->
      is_safe(e, nil) === 0
    end)
    cnt = length(unsafeReps)
    IO.puts("count is: #{cnt}")

    proc1(input) + proc2(unsafeReps, 0)

  end

  def getDiffs(rep=[curr|rest=[next|tail]], acc) do
    acc = acc++[curr - next]
    getDiffs(rest, acc)
  end
  def getDiffs([curr|_], acc) do acc end

  def example do
    input = [
      [1,3,5,7],
      [7,6,3,1],
      [7,5,5,1],
      [1,5,7,9]
    ]
    unsafeReps = Enum.filter(input, fn e->
      is_safe(e, nil) === 0
    end)
    IO.inspect(unsafeReps)
    {proc1(input), proc2(unsafeReps, 0)}
  end

  def proc2([], sum) do sum end
  def proc2([report| rest], sum) do
    safety = isActuallySafe(report,0, length(report) - 1, 0)
    proc2(rest, sum + safety)
  end

  def isActuallySafe(_,_,_,isSafe) when isSafe === 1 do 1 end
  def isActuallySafe(report, i, maxIndex, isSafe) when i > maxIndex do isSafe end
  def isActuallySafe(report, i, maxIndex, isSafe) do
    subRep = List.delete_at(report, i)
    safety = is_safe(subRep, nil)
    #if(safety === 0) do IO.inspect(subRep) end
    isActuallySafe(report, i + 1, maxIndex, safety)
  end



  def proc1([report | rest]) do
    is_safe(report, nil) + proc1(rest)
  end
  def proc1([]) do 0 end

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
