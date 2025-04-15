; ModuleID = 'src/kernel_4.cpp'
source_filename = "src/kernel_4.cpp"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

; Function Attrs: noinline nounwind uwtable
define i32 @_Z8kernel_4iiii(i32 %a, i32 %b, i32 %c, i32 %n) #0 {
entry:
  %a.addr = alloca i32, align 4
  %b.addr = alloca i32, align 4
  %c.addr = alloca i32, align 4
  %n.addr = alloca i32, align 4
  %i = alloca i32, align 4
  store i32 %a, i32* %a.addr, align 4
  store i32 %b, i32* %b.addr, align 4
  store i32 %c, i32* %c.addr, align 4
  store i32 %n, i32* %n.addr, align 4
  store i32 0, i32* %i, align 4
  br label %for.cond

for.cond:                                         ; preds = %for.inc, %entry
  %0 = load i32, i32* %i, align 4
  %cmp = icmp slt i32 %0, 100
  br i1 %cmp, label %for.body, label %for.end

for.body:                                         ; preds = %for.cond
  %1 = load i32, i32* %b.addr, align 4
  %add = add nsw i32 %1, 50
  %2 = load i32, i32* %n.addr, align 4
  %add1 = add nsw i32 100, %2
  %mul = mul nsw i32 %add, %add1
  %3 = load i32, i32* %c.addr, align 4
  %add2 = add nsw i32 40, %3
  %mul3 = mul nsw i32 %mul, %add2
  %4 = load i32, i32* %a.addr, align 4
  %add4 = add nsw i32 10, %4
  %mul5 = mul nsw i32 %mul3, %add4
  store i32 %mul5, i32* %a.addr, align 4
  %5 = load i32, i32* %a.addr, align 4
  %6 = load i32, i32* %n.addr, align 4
  %7 = load i32, i32* %c.addr, align 4
  %add6 = add nsw i32 %6, %7
  %div = sdiv i32 %5, %add6
  store i32 %div, i32* %a.addr, align 4
  %8 = load i32, i32* %b.addr, align 4
  %9 = load i32, i32* %a.addr, align 4
  %10 = load i32, i32* %c.addr, align 4
  %add7 = add nsw i32 %9, %10
  %rem = srem i32 %8, %add7
  store i32 %rem, i32* %a.addr, align 4
  %11 = load i32, i32* %a.addr, align 4
  %12 = load i32, i32* %n.addr, align 4
  %mul8 = mul nsw i32 %11, %12
  %13 = load i32, i32* %c.addr, align 4
  %14 = load i32, i32* %b.addr, align 4
  %add9 = add nsw i32 %13, %14
  %15 = load i32, i32* %b.addr, align 4
  %mul10 = mul nsw i32 %add9, %15
  %xor = xor i32 %mul8, %mul10
  %16 = load i32, i32* %c.addr, align 4
  %add11 = add nsw i32 %16, %xor
  store i32 %add11, i32* %c.addr, align 4
  br label %for.inc

for.inc:                                          ; preds = %for.body
  %17 = load i32, i32* %i, align 4
  %inc = add nsw i32 %17, 1
  store i32 %inc, i32* %i, align 4
  br label %for.cond

for.end:                                          ; preds = %for.cond
  %18 = load i32, i32* %c.addr, align 4
  ret i32 %18
}

; Function Attrs: noinline norecurse nounwind uwtable
define i32 @main() #1 {
entry:
  %a = alloca i32, align 4
  %b = alloca i32, align 4
  %c = alloca i32, align 4
  %i = alloca i32, align 4
  %call = call i32 @rand() #3
  %rem = srem i32 %call, 10
  store i32 %rem, i32* %a, align 4
  %call1 = call i32 @rand() #3
  %rem2 = srem i32 %call1, 10
  store i32 %rem2, i32* %b, align 4
  %call3 = call i32 @rand() #3
  %rem4 = srem i32 %call3, 10
  store i32 %rem4, i32* %c, align 4
  store i32 0, i32* %i, align 4
  %call5 = call i32 @rand() #3
  %rem6 = srem i32 %call5, 10
  store i32 %rem6, i32* %i, align 4
  %0 = load i32, i32* %a, align 4
  %1 = load i32, i32* %b, align 4
  %2 = load i32, i32* %c, align 4
  %3 = load i32, i32* %i, align 4
  %call7 = call i32 @_Z8kernel_4iiii(i32 %0, i32 %1, i32 %2, i32 %3)
  ret i32 0
}

; Function Attrs: nounwind
declare i32 @rand() #2

attributes #0 = { noinline nounwind uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { noinline norecurse nounwind uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { nounwind "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { nounwind }

!llvm.module.flags = !{!0}
!llvm.ident = !{!1}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{!"clang version 6.0.1 (http://github.com/llvm-mirror/clang 2f27999df400d17b33cdd412fdd606a88208dfcc) (http://github.com/llvm-mirror/llvm 5136df4d089a086b70d452160ad5451861269498)"}
