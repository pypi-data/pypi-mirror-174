#ifndef LIBTOQM_SCHEDULEDGATESTACK_HPP
#define LIBTOQM_SCHEDULEDGATESTACK_HPP

#include <memory>
#include <deque>
#include <utility>

namespace toqm {

class ScheduledGate;

class ScheduledGateStack {
public:
	std::shared_ptr<ScheduledGate> value = nullptr;
	std::shared_ptr<ScheduledGateStack> next = nullptr;
	int size = 0;

	ScheduledGateStack();
	~ScheduledGateStack();

	static std::unique_ptr<ScheduledGateStack> push(const std::shared_ptr<ScheduledGateStack> & head, const std::shared_ptr<ScheduledGate>& newVal);

private:
	ScheduledGateStack(std::shared_ptr<ScheduledGate>  value, std::shared_ptr<ScheduledGateStack>  next, int size)
		: value(std::move(value)), next(std::move(next)), size(size) {}
};

}

#endif//LIBTOQM_SCHEDULEDGATESTACK_HPP
