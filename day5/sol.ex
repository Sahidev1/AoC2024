
defmodule Sol do
  @type rules :: %{} | %{key: integer() , set: MapSet.t(integer())}

  def main do
    {rules, updates} = parseInput()
    proc(rules, updates, 0)
  end

  def test do
    {rules, updates} = example()
    proc(rules, updates, 0)
  end

  def proc(rules, updates=[update|rest], sum) do
    medianIndex = div(length(update), 2)
    median = isValidUpdate(rules, update, update, medianIndex, 0, 0)
    proc(rules, rest, sum + median)
  end
  def proc(rules, [], sum) do sum end

  def isValidUpdate(rules, update, [], medianIndex, itercnt, median) do
    median
  end
  def isValidUpdate(rules, update, [curr| rest],  medianIndex, itercnt ,median) do
    median = if (itercnt === medianIndex) do curr else median end

    set = Map.get(rules, curr)
    currIndex = itercnt

    {isValid, i} = (set === nil && {true, 0}) || Enum.reduce_while(update, {true, 0}, fn e,acc ->
      {isValid, i} = acc

      isValid = cond do
          i < currIndex ->
            !MapSet.member?(set, e)
          i > currIndex ->
            MapSet.member?(set, e)
          true -> true
      end

      if(isValid) do {:cont, {true, i + 1}} else {:halt, {false, i}} end
    end)

    if (isValid) do
      isValidUpdate(rules, update,rest, medianIndex, itercnt + 1, median)
    else
      0
    end
  end




  def example do
    data = "47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"

    parse(data)
  end

  def parseInput do
    fPath = "input.txt"
    {:ok, dataStr} = File.read(fPath)
    parse(dataStr)
  end

  def parse(str) do
    [rules, updates] = String.split(str, "\n\n")
    rules = Enum.map(String.split(rules, "\n", trim: true), fn e->
      [a,b] = String.split(e, "|")
      [a, b] = [String.to_integer(a), String.to_integer(b)]
    end)

    ruleMap = Enum.reduce(rules, %{}, fn e, acc ->
      [k, t] = e
      set = if (Map.has_key?(acc, k)) do
        Map.get(acc, k)
      else
        MapSet.new()
      end
      Map.put(acc, k,  MapSet.put(set, t))
    end)
    updates = String.split(updates, "\n", trim: true)
    updates = Enum.map(updates, fn e->
      Enum.map(String.split(e, ","), fn n->
        String.to_integer(n)
      end)
    end)
    {ruleMap, updates}
  end
end